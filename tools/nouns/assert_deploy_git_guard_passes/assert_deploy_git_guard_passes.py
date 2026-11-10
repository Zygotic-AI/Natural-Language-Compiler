"""Temp-git tests for tools/deploy_git_guard.sh."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GUARD = ROOT / "tools" / "deploy_git_guard.sh"
GIT_TEST_NAME = "guard test"
GIT_TEST_EMAIL = "guard@test"


def git_test_env() -> dict[str, str]:
    """Git author/committer env for temp repos (no machine identity required)."""
    merged = os.environ.copy()
    merged["GIT_AUTHOR_NAME"] = GIT_TEST_NAME
    merged["GIT_AUTHOR_EMAIL"] = GIT_TEST_EMAIL
    merged["GIT_COMMITTER_NAME"] = GIT_TEST_NAME
    merged["GIT_COMMITTER_EMAIL"] = GIT_TEST_EMAIL
    return merged


def configure_git_identity(cwd: Path) -> None:
    """Set user.name and user.email on a temp repository."""
    git(cwd, "config", "user.email", GIT_TEST_EMAIL)
    git(cwd, "config", "user.name", GIT_TEST_NAME)


def run_guard(
    cwd: Path,
    *,
    ref: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run deploy_git_guard.sh in cwd with optional DEPLOY_GIT_REF."""
    merged = os.environ.copy()
    merged["DEPLOY_GIT_REMOTE"] = "origin"
    merged["DEPLOY_GIT_BASE"] = "main"
    if ref is not None:
        merged["DEPLOY_GIT_REF"] = ref
    return subprocess.run(
        ["bash", str(GUARD)],
        cwd=str(cwd),
        env=merged,
        capture_output=True,
        text=True,
        check=False,
    )


def git(cwd: Path, *args: str) -> None:
    """Run git in cwd; raise on failure."""
    subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        env=git_test_env(),
        check=True,
        capture_output=True,
        text=True,
    )


def setup_pair(tmp: Path) -> tuple[Path, Path]:
    """Create bare origin and clone."""
    bare = tmp / "origin.git"
    work = tmp / "work"
    work.mkdir()
    git(work, "init", "-b", "main")
    configure_git_identity(work)
    (work / "f").write_text("1\n", encoding="utf-8")
    git(work, "add", "f")
    git(work, "commit", "-m", "c1")
    git(work, "clone", "--bare", ".", str(bare))
    git(tmp, "clone", str(bare), "clone")
    clone = tmp / "clone"
    configure_git_identity(clone)
    return bare, clone


def advance_main_on_origin(bare: Path, extra_commit_msg: str) -> None:
    """Push a new commit onto bare origin/main."""
    with tempfile.TemporaryDirectory() as td:
        w = Path(td) / "w"
        git(Path(td), "clone", str(bare), "w")
        configure_git_identity(w)
        (w / "f").write_text(extra_commit_msg + "\n", encoding="utf-8")
        git(w, "add", "f")
        git(w, "commit", "-m", extra_commit_msg)
        git(w, "push", "origin", "main")


def main() -> int:
    if not GUARD.is_file():
        print("MET:SKIP missing deploy_git_guard.sh", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        bare, clone = setup_pair(tmp)
        advance_main_on_origin(bare, "main-moved")
        proc = run_guard(clone)
        if proc.returncode == 0:
            print(proc.stdout, proc.stderr)
            print("MET:FAIL stale HEAD should refuse", file=sys.stderr)
            return 1

        git(clone, "fetch", "origin", "main")
        git(clone, "merge", "--ff-only", "origin/main")
        proc = run_guard(clone)
        if proc.returncode != 0:
            print(proc.stdout, proc.stderr)
            print("MET:FAIL current main tip should pass", file=sys.stderr)
            return 1

        old_sha = subprocess.run(
            ["git", "rev-parse", "HEAD~1"],
            cwd=str(clone),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        git(clone, "tag", "v0.0.0-test", old_sha)
        proc = run_guard(clone, ref="v0.0.0-test")
        if proc.returncode != 0:
            print(proc.stdout, proc.stderr)
            print("MET:FAIL on-main tag should pass", file=sys.stderr)
            return 1

        orphan = tmp / "orphan"
        git(tmp, "clone", str(bare), "orphan")
        configure_git_identity(orphan)
        git(orphan, "checkout", "--orphan", "side")
        (orphan / "x").write_text("orphan\n", encoding="utf-8")
        git(orphan, "add", "x")
        git(orphan, "commit", "-m", "orphan")
        git(orphan, "tag", "vbad")
        proc = run_guard(orphan, ref="vbad")
        if proc.returncode == 0:
            print(proc.stdout, proc.stderr)
            print("MET:FAIL off-main tag should refuse", file=sys.stderr)
            return 1

    print("MET assert-deploy-git-guard-passes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
