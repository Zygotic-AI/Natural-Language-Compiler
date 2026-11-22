"""ADR 0061 steps 3-6: validate, sign, main, tag (plus notes and statement). One Tree comparison guards main and tag."""
from __future__ import annotations

BOUNDARY = "bba-emit"

import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_requirements import hub_tool  # noqa: E402
from nouns.checker_digest.checker_digest import ARMOR_REL, DIGEST_REL, digest_paths  # noqa: E402
from nouns.owner_sidecar.owner_sidecar import (  # noqa: E402
    OWNER_KEY_REL,
    TRUSTED_REL,
    gpg_verify_clearsigned_plaintext,
    load_trusted_fingerprints_from_text,
)

REPO = "Zygotic-AI/Natural-Language-Compiler"
VERSION_REL = "integrity/nlc-version.json"
KEYS_REL = "integrity/owner-keys"
VERIFIER_REL = "tools/check-checker-digest-signature.py"
ANCHOR = "4c201315267781c179d99da8e56afa638b53ee6b"  # v0.8.0, the last release before ADR 0061
BEGIN = "-----BEGIN PGP SIGNED MESSAGE-----"
END = "-----END PGP SIGNATURE-----"
USAGE = "usage: ./release validate|sign [--armor FILE]|main|tag"
SIGN_BEGIN = (
    "RELEASE_SIGN_BLOCK:BEGIN owner: sign exactly the lines between these markers "
    "as a clearsigned message and paste the result back"
)
SIGN_END = "RELEASE_SIGN_BLOCK:END"
MEMBERS_HEAD = "Members (not signed; the Tree line fixes them):"


def git(*args: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    out = subprocess.run(["git", *args], cwd=cwd or ROOT, env=env, check=True, capture_output=True, text=True)
    return out.stdout.strip()


def refuse(msg: str) -> int:
    print(f"RELEASE:REFUSED {msg}")
    return 1


def tree_without_armor(rev: str) -> str:
    """Tree of rev with the armor file removed: the bytes the owner signs (ADR 0061)."""
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(tmp) / "index")}
        git("read-tree", rev, env=env)
        git("update-index", "--force-remove", ARMOR_REL, env=env)
        return git("write-tree", env=env)


def release_branch() -> tuple[str, str]:
    """On release/vX.Y.Z, clean, nothing local that origin lacks (R7-M2). Returns (branch, version) or raises."""
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if not branch.startswith("release/v"):
        raise Refused(f"run on release/vX.Y.Z, not {branch}")
    if git("status", "--porcelain"):
        raise Refused("worktree is not clean; commit through a change branch or stash")
    git("fetch", "-q", "origin", branch)
    if git("rev-list", "--count", f"origin/{branch}..HEAD") != "0":
        raise Refused(f"HEAD has commits origin/{branch} does not; merge them with a change branch (step 2), then run this again")
    return branch, branch[len("release/v"):]


class Refused(Exception):
    pass


@contextmanager
def worktree(rev: str):
    """Fresh detached worktree of rev; always removed, even when setup fails."""
    with tempfile.TemporaryDirectory() as tmp:
        wt = Path(tmp) / "w"
        try:
            git("worktree", "add", "-q", "--detach", str(wt), rev)
            yield wt
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(wt)], cwd=ROOT, capture_output=True)
            subprocess.run(["git", "worktree", "prune"], cwd=ROOT, capture_output=True)


def run(wt: Path, *cmd: str, quiet: bool = False) -> int:
    out = subprocess.run([sys.executable, *cmd], cwd=wt, stdout=subprocess.DEVNULL if quiet else None)
    return out.returncode


def write_all(wt: Path, ver: str) -> None:
    """Every file validate writes, in order, then staged (the content digest reads tracked files)."""
    steps = [
        ["tools/nlc_release_bump.py", "--align-to", ver],
        ["tools/nlc_release_tag_gate.py", "notes"],
    ]
    for cmd in steps:
        if run(wt, *cmd):
            raise Refused(f"{cmd[0]} failed")
    if run(wt, "tools/nlc_release_notes.py", "--check", "--version", ver):
        raise Refused(f"RELEASE_VALIDATE:CODE_DEFECT docs/adoption/RELEASE-v{ver}.md: merge PRs with gh pr merge --merge so their titles are the notes")
    for cmd in (["tools/derive-check-inputs.py", "--write"], ["tools/nlc.py", "--project", ".", "maintainer", "guide", "before-generate"]):
        if run(wt, *cmd):
            raise Refused(f"{cmd[0]} failed")
    git("add", "-A", cwd=wt)
    for cmd in (["tools/regen-derived-release-state.py"], ["tools/fitness-planit-identity.py", "--record"]):
        if run(wt, *cmd):
            raise Refused(f"{cmd[0]} failed")
    git("add", "-A", cwd=wt)


def suite(wt: Path, log: Path | None = None) -> int:
    cmd = [sys.executable, "tools/nlc.py", "--project", ".", "gate", "--profile", "release"]
    if log is None:
        return subprocess.run(cmd, cwd=wt).returncode
    with log.open("w") as fh:
        rc = subprocess.run(cmd, cwd=wt, stdout=fh, stderr=subprocess.STDOUT).returncode
    if rc:
        print("\n".join(sorted({l for l in log.read_text().splitlines() if l.startswith("CI:FAIL")})))
    return rc


def validate() -> int:
    """Step 3: write everything, commit if anything changed, run the suite, push."""
    try:
        branch, ver = release_branch()
        with worktree(f"origin/{branch}") as wt:
            write_all(wt, ver)
            changed = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=wt).returncode != 0
            if changed or git("log", "-1", "--format=%s", cwd=wt) != f"release: validate v{ver}":
                git("commit", "-q", "--allow-empty", "-m", f"release: validate v{ver}", cwd=wt)
            if suite(wt):
                print("RELEASE_VALIDATE:CODE_DEFECT fix the failing check above in a change branch, then run ./release validate again")
                return 1
            git("push", "-q", "origin", f"HEAD:{branch}", cwd=wt)
        git("merge", "-q", "--ff-only", f"origin/{branch}")
    except Refused as why:
        msg = str(why)
        print(msg if msg.startswith("RELEASE_VALIDATE:") else f"RELEASE:REFUSED {msg}")
        return 1
    print("RELEASE_VALIDATE:ONLY_SIGNATURE_LEFT")
    return statement()


def prove(head: str, ver: str) -> None:
    """R7-B2: HEAD is a passed validate: validate's writes change nothing and the suite passes on HEAD."""
    with worktree(head) as wt:
        write_all(wt, ver)
        changed = git("diff", "--cached", "--name-only", "HEAD", cwd=wt).split()
        if changed:
            raise Refused(f"HEAD is not a validated commit; validate would change {' '.join(changed[:5])}; run ./release validate")
        if suite(wt, wt.parent / "gate.log"):
            raise Refused("the release suite fails on HEAD; run ./release validate")


def version(rev: str) -> str:
    return json.loads(git("show", f"{rev}:{VERSION_REL}"))["version"]


def release_tag_at(commit: str) -> str | None:
    """The tag at commit that names the commit's own version, if any."""
    try:
        want = f"v{version(commit)}"
    except (subprocess.CalledProcessError, ValueError, KeyError):
        return None
    return want if want in git("tag", "--points-at", commit).split() else None


def previous_tag(rev: str, ver: str | None = None) -> tuple[str | None, str]:
    """Trust root for rev (R7-B1): the nearest release tag on rev's first-parent line, not rev's own version.

    Side commits merged in (e.g. with -s ours) are never on the first-parent line. A tag found there is
    trusted only if it is ANCHOR, or if its own commit carries a statement its previous tag's keys verify
    with a Tree equal to that commit's tree. Anything else refuses; the walk never skips a bad tag.
    """
    ver = ver or version(rev)
    for commit in git("rev-list", "--first-parent", rev).split():
        tag = release_tag_at(commit)
        if tag is None or tag == f"v{ver}":
            continue
        if commit == ANCHOR:
            return tag, ""
        want, why = signed_tree(commit)
        if want is None or want != tree_without_armor(commit):
            return None, f"{tag} on the first-parent line is not a verified release ({why or 'Tree differs'})"
        return tag, ""
    return None, "no release tag on the first-parent line"


def verify_clearsigned_with_previous_tag(armor: str, prev: str) -> tuple[str | None, str]:
    """Plaintext of armor, verified with prev's trusted fingerprints and owner key.

    Same path signed_tree uses. Returns (plaintext, "") or (None, one-line reason).
    """
    trusted, terr = load_trusted_fingerprints_from_text(git("show", f"{prev}:{TRUSTED_REL}"))
    if terr:
        return None, f"{prev} keys: {terr}"
    with tempfile.TemporaryDirectory() as tmp:
        asc, key = Path(tmp) / "armor.asc", Path(tmp) / "owner.asc"
        asc.write_text(armor if armor.endswith("\n") else armor + "\n", encoding="utf-8")
        key.write_text(git("show", f"{prev}:{OWNER_KEY_REL}") + "\n", encoding="utf-8")
        _, plaintext, errors = gpg_verify_clearsigned_plaintext(
            asc, trusted_fingerprints=trusted, key_import_paths=[key]
        )
    if errors:
        return None, f"armor does not verify with {prev} keys"
    return plaintext, ""


def signed_tree(rev: str) -> tuple[str | None, str]:
    """Tree field from the armor at rev, read only from plaintext gpg verified with the previous tag's keys."""
    prev, why = previous_tag(rev)
    if prev is None:
        return None, why
    try:
        armor = git("show", f"{rev}:{ARMOR_REL}") + "\n"
    except subprocess.CalledProcessError:
        return None, f"no {ARMOR_REL} at {rev}"
    if not armor.startswith(BEGIN + "\n") or not armor.rstrip().endswith(END):
        return None, "armor has bytes outside the clearsigned block"
    plaintext, why = verify_clearsigned_with_previous_tag(armor, prev)
    if plaintext is None:
        return None, why
    trees = re.findall(r"^Tree: ([0-9a-f]{40})$", plaintext, re.M)
    if len(trees) != 1:
        return None, "verified statement has no single Tree line"
    return trees[0], ""


def tree_guard(rev: str) -> int:
    want, why = signed_tree(rev)
    if want is None:
        return refuse(f"{rev}: {why}")
    have = tree_without_armor(rev)
    if want != have:
        return refuse(f"{rev} tree {have} is not the signed Tree {want}; validate and sign again")
    return 0


def notes() -> int:
    """Rewrite docs/adoption/RELEASE-vX.Y.Z.md from the titles of PRs merged (gh pr merge --merge) since the previous tag."""
    ver = json.loads((ROOT / VERSION_REL).read_text(encoding="utf-8"))["version"]
    prev, why = previous_tag("HEAD", ver)
    if prev is None:
        return refuse(why)
    log = git("log", "--merges", "--first-parent", "--reverse", "--format=%s%x1f%b%x1e", f"{prev}..HEAD")
    lines = []
    for rec in log.split("\x1e"):
        subject, _, body = rec.strip().partition("\x1f")
        m = re.match(r"Merge pull request #(\d+) from ", subject)
        if m and body.strip():
            lines.append(f"- {body.strip().splitlines()[0]} (#{m.group(1)})")
    path = ROOT / "docs" / "adoption" / f"RELEASE-v{ver}.md"
    path.write_text(f"# Natural Language Compiler hub v{ver}\n\n## Highlights\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    return 0


def sign_block() -> str:
    """The seven lines sign() signs: six fields and Tree, each ending in a newline."""
    digest = (ROOT / DIGEST_REL).read_bytes()
    lines = (
        f"Repo: {REPO}",
        f"Document: {DIGEST_REL}",
        f"Content-SHA256: {hashlib.sha256(digest).hexdigest()}",
        "Decision: Accepted",
        f"Date: {datetime.date.today().isoformat()}",
        f"Summary: Ratify release v{version('HEAD')}. This signature covers only these exact bytes.",
        f"Tree: {tree_without_armor('HEAD')}",
    )
    return "".join(f"{line}\n" for line in lines)


def _signed_lines(text: str) -> list[str]:
    """Line text after stripping trailing whitespace, which gpg clearsign does."""
    return [line.rstrip() for line in text.splitlines()]


def _armor_has_outside_bytes(raw: bytes) -> bool:
    """True when any byte sits before BEGIN or after END (a single line ending after END is the line itself)."""
    begin, end = BEGIN.encode("ascii"), END.encode("ascii")
    if not raw.startswith(begin):
        return True
    end_at = raw.rfind(end)
    if end_at < 0:
        return True
    return raw[end_at + len(end):] not in (b"", b"\n", b"\r\n")


def pasted_armor(path: Path) -> bytes:
    """Read a pasted clearsigned message. Raises Refused and writes nothing."""
    try:
        raw = path.read_bytes()
    except OSError:
        raise Refused(f"cannot read armor file {path}") from None
    if _armor_has_outside_bytes(raw):
        raise Refused("armor has bytes outside the clearsigned block")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise Refused("armor is not utf-8") from None
    prev, why = previous_tag("HEAD")
    if prev is None:
        raise Refused(why)
    plaintext, why = verify_clearsigned_with_previous_tag(text, prev)
    if plaintext is None:
        raise Refused(why)
    if _signed_lines(plaintext) != _signed_lines(sign_block()):
        raise Refused("verified plaintext is not the sign block")
    return raw


def statement() -> int:
    """Print the sign block between markers, then the member list, which is not signed."""
    sys.stdout.write(SIGN_BEGIN + "\n")
    sys.stdout.write(sign_block())
    sys.stdout.write(SIGN_END + "\n")
    print("")
    print(MEMBERS_HEAD)
    for rel in digest_paths(ROOT):
        print(f"Member: {rel}")
    return 0


def sign(argv: list[str] | None = None) -> int:
    """Step 4: re-prove validate on the pushed HEAD, then clearsign or take pasted armor, commit, push."""
    args = [] if argv is None else list(argv)
    armor_path: Path | None = None
    if args:
        if len(args) != 2 or args[0] != "--armor":
            print(USAGE)
            return 1
        armor_path = Path(args[1])
    try:
        branch, ver = release_branch()
        head = git("rev-parse", "HEAD")
        if head != git("rev-parse", f"origin/{branch}"):
            raise Refused(f"HEAD is not origin/{branch}; sign only the pushed, validated head")
        if version("HEAD") != ver:
            raise Refused(f"HEAD version is {version('HEAD')}, not {ver}; run ./release validate")
        prove(head, ver)
        if armor_path is None:
            armor = subprocess.run(
                ["gpg", "--clearsign"], input=sign_block(), check=True, capture_output=True, text=True
            ).stdout
            (ROOT / ARMOR_REL).write_text(armor, encoding="utf-8")
        else:
            (ROOT / ARMOR_REL).write_bytes(pasted_armor(armor_path))
    except Refused as why:
        return refuse(str(why))
    git("add", ARMOR_REL)
    git("commit", "-q", "-m", f"release: sign v{ver}")
    git("push", "-q", "origin", f"HEAD:{branch}")
    print("RELEASE_SIGN:DONE")
    return 0


def main_push() -> int:
    """Step 5: push release to main only if it is exactly the signed Tree."""
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if not branch.startswith("release/v"):
        return refuse(f"run on release/vX.Y.Z, not {branch}")
    git("fetch", "-q", "--tags", "origin")
    ref = f"origin/{branch}"
    if tree_guard(ref):
        return 1
    git("push", "-q", "origin", f"{ref}:refs/heads/main")
    print(f"RELEASE_MAIN:DONE {branch} -> main")
    return 0


def tag() -> int:
    """Step 6: Tree must match; previous tag's checker and keys grade origin/main; then tag."""
    git("fetch", "-q", "--tags", "origin")
    if tree_guard("origin/main"):
        return 1
    ver, (prev, _) = version("origin/main"), previous_tag("origin/main")
    with tempfile.TemporaryDirectory() as tmp:
        checker, graded = Path(tmp) / "checker", Path(tmp) / "graded"
        git("worktree", "add", "-q", "--detach", str(checker), prev)
        git("worktree", "add", "-q", "--detach", str(graded), "origin/main")
        try:
            subprocess.run(["rm", "-rf", str(graded / KEYS_REL)], check=True)
            subprocess.run(["cp", "-r", str(checker / KEYS_REL), str(graded / KEYS_REL)], check=True)
            rc = subprocess.run([sys.executable, str(checker / VERIFIER_REL), "--root", str(graded)]).returncode
        finally:
            git("worktree", "remove", "--force", str(checker))
            git("worktree", "remove", "--force", str(graded))
    if rc != 0:
        return refuse(f"{prev} checker did not return MET for origin/main")
    git("tag", "-a", f"v{ver}", "-m", f"v{ver}", "origin/main")
    git("push", "-q", "origin", f"v{ver}")
    print(f"RELEASE_TAG:DONE v{ver} verified by {prev}")
    return 0


def main(argv: list[str] | None = None) -> int:
    hub_tool()
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print(USAGE)
        return 1
    cmd, rest = args[0], args[1:]
    if cmd == "sign":
        return sign(rest)
    commands = {"validate": validate, "main": main_push, "tag": tag, "notes": notes, "statement": statement}
    if rest or cmd not in commands:
        print(USAGE)
        return 1
    return commands[cmd]()


if __name__ == "__main__":
    raise SystemExit(main())
