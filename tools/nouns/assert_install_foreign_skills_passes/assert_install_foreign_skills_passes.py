"""Known-good: hub install MET when ~/.agents/skills already has failing foreign skills.

GitHub issue 67 / ADR 0060: post-install author check grades the hub copied tree
(goals/hub_install/execute.sh staging copy), not every skill under the
shared ~/.agents/skills directory (including a symlink into another project).
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import pty
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXECUTE = ROOT / "goals" / "hub_install" / "execute.sh"
PROMPT = "Lazy-load skills (disable-model-invocation)? y/N"
FOREIGN_SKILL_BODY = """---
name: abbie-command
description: Use when invoking /abbie-command or working with get_template, run_model,
  run_report, or related Abbie tools.
---

# abbie-command

See [prompts](../prompts/README.md).
"""


def _write_foreign_skill(skill_dir: Path) -> Path:
    skill_dir.mkdir(parents=True, exist_ok=True)
    path = skill_dir / "SKILL.md"
    path.write_text(FOREIGN_SKILL_BODY, encoding="utf-8")
    return path


def _install_env(home: Path, store: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["USERPROFILE"] = str(home)
    env["NLC_INSTALL_ROOT"] = str(store)
    env["NLC_INSTALL_SCOPE"] = "global"
    env["CI"] = "1"
    env["NLC_SKIP_VERIFY"] = "1"
    env.pop("NLC_REF", None)
    env.pop("NLC_VERSION", None)
    return env


def _run_install(home: Path, store: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(EXECUTE), "--global"],
        cwd=str(ROOT),
        env=_install_env(home, store),
        capture_output=True,
        text=True,
        check=False,
    )


def _invocation_flag(path: Path) -> str | None:
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("disable-model-invocation:"):
            return line.split(":", 1)[1].strip()
    return None


def _prepare_cursor(home: Path) -> None:
    _write_foreign_skill(home / ".cursor" / "skills" / "abbie-command")


def _assert_flags(label: str, home: Path, store: Path, expected: str) -> str | None:
    planit = home / ".agents" / "skills" / "planit" / "SKILL.md"
    foreign = home / ".agents" / "skills" / "abbie-command" / "SKILL.md"
    hub_planit = store / "hub" / ".agents" / "skills" / "planit" / "SKILL.md"
    cursor_planit = home / ".cursor" / "skills" / "planit" / "SKILL.md"
    cursor_foreign = home / ".cursor" / "skills" / "abbie-command" / "SKILL.md"
    if _invocation_flag(planit) != expected:
        return f"{label}: installed planit flag {_invocation_flag(planit)!r}, expected {expected}"
    if _invocation_flag(foreign) is not None:
        return f"{label}: foreign skill gained disable-model-invocation"
    if _invocation_flag(hub_planit) != "true":
        return f"{label}: hub tree flag changed to {_invocation_flag(hub_planit)!r}"
    if _invocation_flag(cursor_planit) != expected:
        return f"{label}: cursor planit flag {_invocation_flag(cursor_planit)!r}, expected {expected}"
    if cursor_foreign.read_text(encoding="utf-8") != FOREIGN_SKILL_BODY:
        return f"{label}: cursor foreign skill was rewritten"
    return None


def _assert_install_ok(label: str, home: Path, store: Path, proc: subprocess.CompletedProcess[str]) -> str | None:
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        return f"{label}: install exit {proc.returncode}\n{out[-1600:]}"
    if "INSTALL:NOT_MET" in out:
        return f"{label}: INSTALL:NOT_MET in output\n{out[-1600:]}"
    if "SKILL_AUTHOR:MET" not in out:
        return f"{label}: missing SKILL_AUTHOR:MET\n{out[-1600:]}"
    if "VIOLATION frontmatter-yaml" in out or "VIOLATION in-skill-links" in out:
        return f"{label}: author check still graded foreign skills\n{out[-1600:]}"
    if PROMPT in out:
        return f"{label}: prompted while non-interactive"
    if "lazy-load: false" not in out:
        return f"{label}: missing lazy-load: false\n{out[-800:]}"
    planit = home / ".agents" / "skills" / "planit" / "SKILL.md"
    foreign = home / ".agents" / "skills" / "abbie-command" / "SKILL.md"
    if not planit.is_file():
        return f"{label}: hub planit skill missing after overlay ({planit})"
    if not foreign.is_file():
        return f"{label}: foreign skill missing after overlay ({foreign})"
    return _assert_flags(label, home, store, "false")


def _test_symlink_dest(base: Path) -> str | None:
    home = base / "home-link"
    other = base / "other-skills"
    store = base / "store-link"
    _write_foreign_skill(other / "abbie-command")
    _prepare_cursor(home)
    agents = home / ".agents"
    agents.mkdir(parents=True)
    (agents / "skills").symlink_to(other)
    proc = _run_install(home, store)
    return _assert_install_ok("symlink dest", home, store, proc)


def _test_sibling_dir(base: Path) -> str | None:
    home = base / "home-sib"
    store = base / "store-sib"
    _write_foreign_skill(home / ".agents" / "skills" / "abbie-command")
    _prepare_cursor(home)
    proc = _run_install(home, store)
    return _assert_install_ok("sibling dir", home, store, proc)


def _run_install_answer(home: Path, store: Path, answer: bytes) -> tuple[int, str]:
    env = _install_env(home, store)
    env.pop("CI", None)
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(ROOT)
        os.execvpe("bash", ["bash", str(EXECUTE), "--global"], env)
        os._exit(127)
    os.set_blocking(fd, False)
    buf = bytearray()
    sent = False
    deadline = time.monotonic() + 180
    status: int | None = None
    while time.monotonic() < deadline:
        try:
            chunk = os.read(fd, 4096)
        except BlockingIOError:
            chunk = b""
        except OSError:
            chunk = b""
        if chunk:
            buf += chunk
            if not sent and PROMPT.encode() in buf:
                os.write(fd, answer)
                sent = True
        wpid, st = os.waitpid(pid, os.WNOHANG)
        if wpid != 0:
            status = st
            break
        if not chunk:
            time.sleep(0.05)
    if status is None:
        os.kill(pid, 15)
        os.waitpid(pid, 0)
        os.close(fd)
        return 124, buf.decode(errors="replace")
    while True:
        try:
            chunk = os.read(fd, 4096)
        except (BlockingIOError, OSError):
            break
        if not chunk:
            break
        buf += chunk
    os.close(fd)
    return os.waitstatus_to_exitcode(status), buf.decode(errors="replace")


def _test_interactive_yes(base: Path) -> str | None:
    home = base / "home-yes"
    store = base / "store-yes"
    _write_foreign_skill(home / ".agents" / "skills" / "abbie-command")
    _prepare_cursor(home)
    code, out = _run_install_answer(home, store, b"y\n")
    if code != 0:
        return f"interactive yes: install exit {code}\n{out[-1600:]}"
    if PROMPT not in out:
        return f"interactive yes: prompt missing\n{out[-800:]}"
    if "lazy-load: true" not in out:
        return f"interactive yes: missing lazy-load: true\n{out[-800:]}"
    if "SKILL_AUTHOR:MET" not in out:
        return f"interactive yes: missing SKILL_AUTHOR:MET\n{out[-800:]}"
    return _assert_flags("interactive yes", home, store, "true")


def main() -> int:
    if not EXECUTE.is_file():
        print("ASSERT:FAIL missing goals/hub_install/execute.sh")
        return 1
    with tempfile.TemporaryDirectory(prefix="nlc-foreign-skills-") as tmp:
        base = Path(tmp)
        for err in (_test_symlink_dest(base), _test_sibling_dir(base), _test_interactive_yes(base)):
            if err:
                print(f"ASSERT:FAIL {err}")
                return 1
    print("ASSERT:PASS install MET with failing foreign skills already present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
