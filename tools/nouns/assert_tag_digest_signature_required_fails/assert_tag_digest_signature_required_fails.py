"""Known-bad: an unsigned checker digest is refused once the tag verifier exists.

Also grades `./release sign --armor`: a throwaway key, the way the ADR signature
fixture builds one, must refuse a different block, a byte outside the armor, and
an armor that does not verify, and must accept an armor of the sign block.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import io
import json
import os
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
ARMOR_REL = "integrity/checker-digest.sha256.approval.asc"


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def _run(argv: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, env=env, capture_output=True, text=True, check=False)


def _make_key(home: Path, name: str) -> str:
    """Throwaway signing key, same batch shape as assert_adr_detached_sig_fails."""
    home.mkdir(parents=True, exist_ok=True)
    os.chmod(home, 0o700)
    conf = home / "key.conf"
    conf.write_text(
        "%no-protection\nKey-Type: EDDSA\nKey-Curve: ed25519\nKey-Usage: sign\n"
        f"Name-Real: {name}\nName-Email: {name}@example.invalid\nExpire-Date: 1d\n",
        encoding="utf-8",
    )
    env = {**os.environ, "GNUPGHOME": str(home)}
    gen = _run(["gpg", "--batch", "--generate-key", str(conf)], env=env)
    if gen.returncode != 0:
        raise RuntimeError(gen.stderr or gen.stdout)
    listed = _run(["gpg", "--list-secret-keys", "--with-colons"], env=env)
    for line in (listed.stdout or "").splitlines():
        parts = line.split(":")
        if parts and parts[0] == "fpr":
            return parts[9]
    raise RuntimeError("no fingerprint")


def _clearsign(home: Path, body: str, dest: Path) -> None:
    env = {**os.environ, "GNUPGHOME": str(home)}
    dest.parent.mkdir(parents=True, exist_ok=True)
    src = dest.with_suffix(dest.suffix + ".txt")
    src.write_text(body, encoding="utf-8")
    proc = _run(["gpg", "--batch", "--yes", "--clearsign", "--output", str(dest), str(src)], env=env)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    src.unlink(missing_ok=True)


def _statement_ok() -> tuple[bool, str]:
    from nouns.nlc_release_tag_gate import nlc_release_tag_gate as gate

    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = gate.statement()
    text = buf.getvalue()
    block = gate.sign_block()
    prefix = gate.SIGN_BEGIN + "\n" + block + gate.SIGN_END + "\n\n" + gate.MEMBERS_HEAD + "\n"
    if rc != 0:
        return False, f"statement exit {rc}"
    if block.count("\n") != 7 or not block.endswith("\n") or "\n\n" in block:
        return False, "sign block is not seven newline-terminated lines"
    if not text.startswith(prefix):
        return False, "statement does not place the sign block between the markers"
    rest = text[len(prefix):]
    member_lines = rest.splitlines()
    if not member_lines or any(not line.startswith("Member: ") for line in member_lines):
        return False, "member lines are not the Member: list"
    return True, "statement prints one sign block then the member list"


def _armor_cases() -> tuple[bool, str]:
    """`--armor` on a local origin. prove() is left as-is in the product; here it is a no-op so this landmine does not re-enter the release gate."""
    from nouns.nlc_release_tag_gate import nlc_release_tag_gate as gate

    source = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
    source_head = source.stdout.strip()
    with tempfile.TemporaryDirectory(prefix="nlc-sign-armor-") as tmp:
        tmp_path = Path(tmp)
        clone = tmp_path / "r"
        bare = tmp_path / "origin.git"
        cloned = subprocess.run(["git", "clone", "--local", "-q", str(ROOT), str(clone)], capture_output=True, text=True)
        if cloned.returncode != 0:
            return False, f"clone --local: {cloned.stderr.strip()}"
        subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
        subprocess.run(["git", "-C", str(clone), "remote", "set-url", "origin", str(bare)], check=True)
        origin = subprocess.run(["git", "-C", str(clone), "remote", "get-url", "origin"], capture_output=True, text=True, check=True).stdout.strip()
        if origin != str(bare):
            return False, f"origin is {origin}"
        shown = subprocess.run(
            ["git", "-C", str(clone), "show", f"{source_head}:integrity/nlc-version.json"],
            capture_output=True, text=True, check=True,
        )
        ver = json.loads(shown.stdout)["version"]
        branch = f"release/v{ver}"
        subprocess.run(["git", "-C", str(clone), "checkout", "-q", "-B", branch, source_head], check=True)
        for key, value in (("user.email", "kb@example.invalid"), ("user.name", "kb"), ("commit.gpgsign", "false")):
            subprocess.run(["git", "-C", str(clone), "config", key, value], check=True)
        prev_ver = "0.8.0" if ver != "0.8.0" else "0.7.0"
        home_a = tmp_path / "gpg-a"
        home_b = tmp_path / "gpg-b"
        fp_a = _make_key(home_a, "sign-a")
        _make_key(home_b, "sign-b")
        env_a = {**os.environ, "GNUPGHOME": str(home_a)}
        exported = _run(["gpg", "--armor", "--export", fp_a], env=env_a)
        if exported.returncode != 0:
            return False, exported.stderr or exported.stdout
        (clone / "integrity/owner-keys/richard-pickett.asc").write_text(exported.stdout, encoding="utf-8")
        (clone / "integrity/owner-keys/TRUSTED_FINGERPRINTS").write_text(f"# scratch pin\n{fp_a}\n", encoding="utf-8")
        ver_path = clone / "integrity/nlc-version.json"
        original_ver = ver_path.read_bytes()
        ver_path.write_text(json.dumps({"version": prev_ver}) + "\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(clone), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(clone), "commit", "-q", "-m", "test: previous release keys"], check=True)
        c_prev = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        subprocess.run(["git", "-C", str(clone), "tag", "-f", f"v{prev_ver}", c_prev], check=True, capture_output=True, text=True)
        ver_path.write_bytes(original_ver)
        subprocess.run(["git", "-C", str(clone), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(clone), "commit", "-q", "-m", "test: release head"], check=True)
        subprocess.run(["git", "-C", str(clone), "push", "-q", "origin", f"HEAD:{branch}"], check=True)
        saved = (gate.ROOT, gate.ANCHOR, gate.prove)
        gate.ROOT = clone
        gate.ANCHOR = c_prev
        gate.prove = lambda _head, _ver: None
        try:
            block = gate.sign_block()
            armors = tmp_path / "armors"
            good = armors / "good.asc"
            other = armors / "other.asc"
            wrong_key = armors / "wrong-key.asc"
            _clearsign(home_a, block, good)
            _clearsign(home_a, block.replace("Decision: Accepted", "Decision: Rejected"), other)
            outside = armors / "outside.asc"
            outside.write_bytes(good.read_bytes() + b"x")
            _clearsign(home_b, block, wrong_key)
            failures: list[str] = []

            def snapshot() -> tuple[str, str, str, bytes]:
                head = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
                remote = subprocess.run(["git", "-C", str(clone), "rev-parse", f"origin/{branch}"], capture_output=True, text=True, check=True).stdout.strip()
                porcelain = subprocess.run(["git", "-C", str(clone), "status", "--porcelain"], capture_output=True, text=True, check=True).stdout
                body = (clone / ARMOR_REL).read_bytes() if (clone / ARMOR_REL).is_file() else b""
                return head, remote, porcelain, body

            def refuse(path: Path, needle: str, label: str) -> None:
                before = snapshot()
                buf = io.StringIO()
                with redirect_stdout(buf):
                    rc = gate.main(["sign", "--armor", str(path)])
                out = buf.getvalue()
                lines = out.splitlines()
                if rc != 1 or len(lines) != 1 or needle not in lines[0] or snapshot() != before:
                    failures.append(f"{label}: rc={rc} out={out!r} moved={snapshot() != before}")

            refuse(other, "verified plaintext is not the sign block", "different block")
            refuse(outside, "armor has bytes outside the clearsigned block", "byte outside")
            refuse(wrong_key, "armor does not verify", "does not verify")
            if failures:
                return False, "; ".join(failures)
            before_head = snapshot()[0]
            good_bytes = good.read_bytes()
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = gate.main(["sign", "--armor", str(good)])
            out = buf.getvalue()
            head, remote, porcelain, body = snapshot()
            subject = subprocess.run(["git", "-C", str(clone), "log", "-1", "--format=%s"], capture_output=True, text=True, check=True).stdout.strip()
            if rc != 0 or out != "RELEASE_SIGN:DONE\n" or body != good_bytes or head == before_head or head != remote or porcelain or subject != f"release: sign v{ver}":
                return False, f"accept rc={rc} out={out!r} subject={subject!r} porcelain={porcelain!r} head_moved={head != before_head} pushed={head == remote} bytes={body == good_bytes}"
        finally:
            gate.ROOT, gate.ANCHOR, gate.prove = saved
    return True, "sign --armor refuses a different block, a byte outside, and an unverified armor, and accepts the sign block"


def main() -> int:
    """Grade a detached copy with the signature file removed.

    The live tree may already carry a valid sidecar. This landmine still has
    to prove that a tree without that sidecar is refused.
    """
    with tempfile.TemporaryDirectory(prefix="nlc-unsigned-digest-") as tmp:
        work = Path(tmp) / "tree"
        added = _git("worktree", "add", "--detach", str(work), "HEAD")
        if added.returncode != 0:
            print(f"ASSERT:FAIL unsigned worktree: {added.stderr.strip()}")
            return 1
        try:
            armor = work / ARMOR_REL
            if armor.is_file():
                armor.unlink()
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "check-checker-digest-signature.py"),
                    "--root",
                    str(work),
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
        finally:
            _git("worktree", "remove", "--force", str(work))
    blob = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0 or "CHECKER_DIGEST_SIGNATURE:NOT_MET" not in blob:
        print(f"ASSERT:FAIL tag verifier accepted unsigned digest: {blob}")
        return 1
    if "missing sidecar" not in blob:
        print(f"ASSERT:FAIL unsigned digest was refused for another reason: {blob}")
        return 1
    print("ASSERT:PASS unsigned checker digest is refused by the tag verifier")
    ok, detail = _statement_ok()
    print(f"ASSERT:{'PASS' if ok else 'FAIL'} {detail}")
    if not ok:
        return 1
    ok, detail = _armor_cases()
    print(f"ASSERT:{'PASS' if ok else 'FAIL'} {detail}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
