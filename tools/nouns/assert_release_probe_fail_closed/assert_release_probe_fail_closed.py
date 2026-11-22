"""Known-bad and known-good probes for the 9 fail-closed release-tool instances still in use (ADR 0061)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import stat
import subprocess
import sys
import tempfile
import urllib.error
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.release_probe.release_probe import ProbeFailure  # noqa: E402

INSTANCES = (
    "tag-exists",
    "list-version-tags",
    "tag-is-ancestor",
    "remote-tag-commit-only",
    "align-local-tag-to-remote",
    "changelog-tag-exists",
    "is-resolvable-commit",
    "git-changed-paths",
    "github-latest-tag",
)

SHA = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
SHA2 = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


def _fail(msg: str) -> int:
    print(f"ASSERT:FAIL {msg}")
    return 1


def _ok(msg: str) -> int:
    print(f"ASSERT:PASS {msg}")
    return 0


def _proc(rc: int, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=["git"], returncode=rc, stdout=stdout, stderr=stderr)


BASH = "/usr/bin/bash"


def _missing(argv: list[str] | None = None, **_kwargs: object) -> subprocess.CompletedProcess[str]:
    raise FileNotFoundError((argv or ["git"])[0])


def _empty(argv: list[str] | None = None, **_kwargs: object) -> subprocess.CompletedProcess[str]:
    return _proc(0, "")


def _boom(argv: list[str] | None = None, **_kwargs: object) -> subprocess.CompletedProcess[str]:
    return _proc(128, "", "fatal: unexpected")


def _scripted(answers: list[object]) -> Callable[..., subprocess.CompletedProcess[str]]:
    queue = list(answers)

    def runner(argv: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        if not queue:
            raise AssertionError(f"no scripted answer left for {argv}")
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        if callable(item):
            return item(argv, **_kwargs)
        return item  # type: ignore[return-value]

    return runner


def _init_repo(path: Path) -> str:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "probe@example.invalid"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "probe"], cwd=path, check=True)
    (path / "f").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "add", "f"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "first"], cwd=path, check=True, capture_output=True)
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=path, check=True, capture_output=True, text=True
    )
    return proc.stdout.strip()


def _kinds_via_runner(
    call: Callable[..., object], kinds: set[str]
) -> str | None:
    mapping = {
        "missing_tool": _missing,
        "empty": _empty,
        "unexpected_error": _boom,
    }
    for kind in kinds:
        try:
            result = call(runner=mapping[kind])
        except ProbeFailure as exc:
            if exc.kind != kind:
                return f"wanted kind={kind} got {exc.kind}: {exc}"
            continue
        return f"wanted ProbeFailure kind={kind}, got {result!r}"
    return None


def fails_tag_exists() -> int:
    from nouns.release_tags import tag_exists

    err = _kinds_via_runner(
        lambda runner: tag_exists("v1.0.0", root=ROOT, runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("tag-exists refuses")


def passes_tag_exists() -> int:
    from nouns.release_tags import tag_exists

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        sha = _init_repo(repo)
        subprocess.run(["git", "tag", "-a", "v9.9.9", "-m", "t", sha], cwd=repo, check=True)
        if not tag_exists("v9.9.9", root=repo):
            return _fail("annotated tag must exist")
        if tag_exists("v0.0.0", root=repo):
            return _fail("missing tag must be confirmed false")
    return _ok("tag-exists known-good")


def fails_list_version_tags() -> int:
    from nouns.release_tags import list_version_tags

    err = _kinds_via_runner(
        lambda runner: list_version_tags(root=ROOT, runner=runner),
        {"missing_tool", "unexpected_error"},
    )
    return _fail(err) if err else _ok("list-version-tags refuses")


def passes_list_version_tags() -> int:
    from nouns.release_tags import list_version_tags

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        sha = _init_repo(repo)
        subprocess.run(["git", "tag", "v1.2.3", sha], cwd=repo, check=True)
        tags = list_version_tags(root=repo)
        if tags != ["v1.2.3"]:
            return _fail(f"expected [v1.2.3] got {tags}")
    return _ok("list-version-tags known-good")


def fails_tag_is_ancestor() -> int:
    from nouns.release_tags import tag_is_ancestor

    err = _kinds_via_runner(
        lambda runner: tag_is_ancestor("v1.0.0", "HEAD", root=ROOT, runner=runner),
        {"missing_tool", "unexpected_error"},
    )
    return _fail(err) if err else _ok("tag-is-ancestor refuses")


def passes_tag_is_ancestor() -> int:
    from nouns.release_tags import tag_is_ancestor

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        sha = _init_repo(repo)
        subprocess.run(["git", "tag", "v1.2.3", sha], cwd=repo, check=True)
        if not tag_is_ancestor("v1.2.3", "HEAD", root=repo):
            return _fail("tag on HEAD must be ancestor")
    return _ok("tag-is-ancestor known-good")


def fails_remote_tag_commit_only() -> int:
    from nouns.release_tags import remote_tag_commit_only

    err = _kinds_via_runner(
        lambda runner: remote_tag_commit_only("v1.0.0", root=ROOT, runner=runner),
        {"missing_tool", "unexpected_error"},
    )
    return _fail(err) if err else _ok("remote-tag-commit-only refuses")


def passes_remote_tag_commit_only() -> int:
    from nouns.release_tags import remote_tag_commit_only

    runner = _scripted([_proc(0, ""), _proc(0, f"{SHA}\trefs/tags/v1.2.3\n")])
    got = remote_tag_commit_only("v1.2.3", runner=runner)
    if got != SHA:
        return _fail(f"expected {SHA} got {got}")
    empty = remote_tag_commit_only("v1.2.3", runner=_scripted([_proc(0, ""), _proc(0, "")]))
    if empty != "":
        return _fail("confirmed absent remote tag must be empty string")
    return _ok("remote-tag-commit-only known-good")


def fails_align_local_tag_to_remote() -> int:
    from nouns.release_tags import align_local_tag_to_remote

    # Divergence confirmed, then fetch missing / empty / unexpected.
    def call(kind: str, runner: object) -> object:
        answers: list[object] = [
            _proc(0, SHA + "\n"),
            _proc(0, ""),
            _proc(0, SHA2 + "\trefs/tags/v1.0.0\n"),
            runner,
        ]
        if kind == "empty":
            answers.append(runner)
        return align_local_tag_to_remote("v1.0.0", root=ROOT, runner=_scripted(answers))

    for kind, runner in (
        ("missing_tool", _missing),
        ("empty", _empty),
        ("unexpected_error", _boom),
    ):
        try:
            result = call(kind, runner)
        except ProbeFailure as exc:
            if exc.kind != kind:
                return _fail(f"align wanted {kind} got {exc.kind}: {exc}")
            continue
        return _fail(f"align wanted refuse kind={kind}, got {result!r}")
    return _ok("align-local-tag-to-remote refuses")


def passes_align_local_tag_to_remote() -> int:
    from nouns.release_tags import align_local_tag_to_remote

    runner = _scripted(
        [
            _proc(0, SHA + "\n"),
            _proc(0, ""),
            _proc(0, SHA2 + "\trefs/tags/v1.0.0\n"),
            _proc(0, ""),
            _proc(0, SHA2 + "\n"),
        ]
    )
    got = align_local_tag_to_remote("v1.0.0", runner=runner)
    if got != SHA2:
        return _fail(f"align should return remote peel {SHA2} got {got}")
    return _ok("align-local-tag-to-remote known-good")


def fails_changelog_tag_exists() -> int:
    from nouns.release_notes import resolve_changelog_from_tag

    err = _kinds_via_runner(
        lambda runner: resolve_changelog_from_tag("v1.0.0", runner=runner, root=ROOT),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("changelog-tag-exists refuses")


def passes_changelog_tag_exists() -> int:
    from nouns.release_notes import resolve_changelog_from_tag

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        sha = _init_repo(repo)
        subprocess.run(["git", "tag", "v1.2.3", sha], cwd=repo, check=True)
        kept = resolve_changelog_from_tag("v1.2.3", root=repo)
        if kept != "v1.2.3":
            return _fail(f"existing from_tag must stay, got {kept}")
        gone = resolve_changelog_from_tag("v9.9.9", root=repo)
        if gone is not None:
            return _fail("confirmed missing from_tag must clear")
    return _ok("changelog-tag-exists known-good")


def fails_is_resolvable_commit() -> int:
    from nouns.evidence_ref.evidence_ref import is_resolvable_commit

    err = _kinds_via_runner(
        lambda runner: is_resolvable_commit(ROOT, SHA, runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("is-resolvable-commit refuses")


def passes_is_resolvable_commit() -> int:
    from nouns.evidence_ref.evidence_ref import is_resolvable_commit

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        sha = _init_repo(repo)
        if not is_resolvable_commit(repo, sha):
            return _fail("real commit must resolve")
        if is_resolvable_commit(repo, "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"):
            return _fail("dangling commit must be confirmed false")
    return _ok("is-resolvable-commit known-good")


def fails_git_changed_paths() -> int:
    from nouns.mandated_paths.mandated_paths import git_changed_paths

    err = _kinds_via_runner(
        lambda runner: git_changed_paths(ROOT, runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("git-changed-paths refuses")


def passes_git_changed_paths() -> int:
    from nouns.mandated_paths.mandated_paths import git_changed_paths

    runner = _scripted([_proc(0, SHA + "\n"), _proc(0, "a.py\n"), _proc(0, ""), _proc(0, "")])
    paths = git_changed_paths(ROOT, runner=runner)
    if paths != ["a.py"]:
        return _fail(f"expected [a.py] got {paths}")
    return _ok("git-changed-paths known-good")


class _Http:
    def __init__(self, exc: BaseException | None = None, body: str = "") -> None:
        self.exc = exc
        self.body = body

    def __call__(self, req: object, timeout: int = 60) -> object:
        if self.exc:
            raise self.exc
        return self

    def __enter__(self) -> "_Http":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body.encode("utf-8")


def fails_github_latest_tag() -> int:
    from nouns.nlc_distribution.nlc_distribution import _github_latest_tag

    try:
        _github_latest_tag("org/repo", opener=_Http(urllib.error.HTTPError("u", 401, "no", {}, None)))
        return _fail("HTTP 401 must refuse")
    except ProbeFailure as exc:
        if exc.kind != "unexpected_error":
            return _fail(f"401 kind {exc.kind}")
    try:
        _github_latest_tag("org/repo", opener=_Http(body=""))
        return _fail("empty HTTP body must refuse")
    except ProbeFailure as exc:
        if exc.kind != "empty":
            return _fail(f"empty kind {exc.kind}")
    try:
        _github_latest_tag(
            "org/repo",
            opener=_Http(urllib.error.HTTPError("u", 404, "no", {}, None)),
            runner=_missing,
        )
        return _fail("404 plus missing git must refuse")
    except ProbeFailure as exc:
        if exc.kind != "missing_tool":
            return _fail(f"404 fallback kind {exc.kind}")
    return _ok("github-latest-tag refuses")


def passes_github_latest_tag() -> int:
    from nouns.nlc_distribution.nlc_distribution import _github_latest_tag

    got = _github_latest_tag("org/repo", opener=_Http(body='{"tag_name":"v1.2.3"}'))
    if got != "1.2.3":
        return _fail(f"expected 1.2.3 got {got}")
    return _ok("github-latest-tag known-good")


_FAILS = {
    "tag-exists": fails_tag_exists,
    "list-version-tags": fails_list_version_tags,
    "tag-is-ancestor": fails_tag_is_ancestor,
    "remote-tag-commit-only": fails_remote_tag_commit_only,
    "align-local-tag-to-remote": fails_align_local_tag_to_remote,
    "changelog-tag-exists": fails_changelog_tag_exists,
    "is-resolvable-commit": fails_is_resolvable_commit,
    "git-changed-paths": fails_git_changed_paths,
    "github-latest-tag": fails_github_latest_tag,
}

_PASSES = {
    "tag-exists": passes_tag_exists,
    "list-version-tags": passes_list_version_tags,
    "tag-is-ancestor": passes_tag_is_ancestor,
    "remote-tag-commit-only": passes_remote_tag_commit_only,
    "align-local-tag-to-remote": passes_align_local_tag_to_remote,
    "changelog-tag-exists": passes_changelog_tag_exists,
    "is-resolvable-commit": passes_is_resolvable_commit,
    "git-changed-paths": passes_git_changed_paths,
    "github-latest-tag": passes_github_latest_tag,
}


def run(instance: str, mode: str) -> int:
    if instance not in INSTANCES:
        return _fail(f"unknown instance {instance}")
    if mode == "fails":
        return _FAILS[instance]()
    if mode == "passes":
        return _PASSES[instance]()
    return _fail(f"unknown mode {mode}")


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2:
        print("usage: assert_release_probe_fail_closed <instance> fails|passes", file=sys.stderr)
        return 2
    return run(args[0], args[1])


if __name__ == "__main__":
    raise SystemExit(main())
