"""Prove a harness loaded this repository's Planit skill."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

CANONICAL_PATH = ".agents/skills/planit/SKILL.md"
REGISTRY_REL = "integrity/planit-skill-registry.json"
EVIDENCE_REL = ".nlc/planit-change-evidence.json"
_SKIP = {".git", "__pycache__", ".venv", "venv", "node_modules", "dist"}
_EXTERNAL_PLANIT_MARKERS = ("~/.agents/skills/planit",)
_ROUTE_SCAN_PREFIXES = (
    ".agents/",
    "docs/",
    "integrity/",
    "adrs/",
    "content-types/",
    "agents/",
)
_ROUTE_SCAN_EXCLUDE_PREFIXES = (
    "docs/rca/",
    "docs/history/",
    "adrs/history/",
)
_ROUTE_SCAN_ROOT_FILES = ("AGENTS.md", "CHARTER.md", "TODO", "DESCRIBE.md")
_ROUTE_IGNORE_FILES = (
    "tools/assert-planit-second-skill-fails.py",
    "tools/assert-planit-external-route-fails.py",
    "tools/assert-planit-other-skill-fails.py",
    "tools/nouns/planit_identity/planit_identity.py",
)
_PLANIT_SKILL_REF = re.compile(r"(?<![\w-])([\w./~-]+/planit/SKILL\.md)")


def content_hash(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def load_registry(root: Path) -> dict[str, object]:
    payload = json.loads((root / REGISTRY_REL).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {}
    return payload


def registry_from_bytes(root: Path) -> dict[str, object]:
    """Derive the Planit identity registry from canonical skill bytes."""
    body = (root / CANONICAL_PATH).read_bytes()
    return {
        "schema": 1,
        "canonical_path": CANONICAL_PATH,
        "content_sha256": content_hash(body),
    }


def write_registry_from_bytes(root: Path) -> Path:
    """Write integrity/planit-skill-registry.json from current skill bytes."""
    dest = root / REGISTRY_REL
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(registry_from_bytes(root), indent=2) + "\n", encoding="utf-8")
    return dest


def identity_errors(registry: dict[str, object], loaded_path: str, loaded: bytes) -> list[str]:
    errors: list[str] = []
    if loaded_path != registry.get("canonical_path"):
        errors.append("loaded path is not the canonical Planit skill")
    if content_hash(loaded) != registry.get("content_sha256"):
        errors.append("loaded Planit skill hash does not match the registry")
    return errors


def handoff_errors(record: dict[str, object], registry: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if record.get("planit_skill_path") != registry.get("canonical_path"):
        errors.append("handoff Planit path does not match the registry")
    if record.get("planit_skill_sha256") != registry.get("content_sha256"):
        errors.append("handoff Planit hash does not match the registry")
    return errors


def source_tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    paths: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in _SKIP for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        if rel == EVIDENCE_REL:
            continue
        paths.append(rel)
    for rel in sorted(paths):
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update((root / rel).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def evidence_errors(root: Path, registry: dict[str, object]) -> list[str]:
    path = root / EVIDENCE_REL
    if not path.is_file():
        return ["missing Planit change evidence"]
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        return ["Planit change evidence must be an object"]
    errors = handoff_errors(record, registry)
    if record.get("source_tree_sha256") != source_tree_hash(root):
        errors.append("Planit change evidence does not match the current tree")
    return errors


def prove(root: Path, loaded_path: str) -> list[str]:
    registry = load_registry(root)
    loaded = (root / loaded_path).read_bytes()
    return identity_errors(registry, loaded_path, loaded)


def loaded_skill_errors(hub: Path, loaded_file: Path) -> list[str]:
    """Hash the skill file the agent loaded against the registry in the hub.

    The product repo is not a registry location. A non-hub project is not a skip.
    """
    registry_path = hub / REGISTRY_REL
    if not registry_path.is_file():
        return [f"missing hub registry {registry_path}"]
    try:
        registry = load_registry(hub)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"hub registry unreadable {registry_path}: {exc}"]
    if not loaded_file.is_file():
        return [f"loaded Planit skill missing {loaded_file}"]
    expected = registry.get("content_sha256")
    if content_hash(loaded_file.read_bytes()) != expected:
        return [f"loaded Planit skill hash does not match hub registry {registry_path}"]
    return []


def _git_ls_files(root: Path, *extra: str) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files", *extra],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [ln.strip().replace("\\", "/") for ln in (proc.stdout or "").splitlines() if ln.strip()]


def on_disk_planit_skill_paths(root: Path) -> list[str]:
    """Return repo-relative paths to every planit/SKILL.md on disk."""
    found: list[str] = []
    for path in root.rglob("SKILL.md"):
        if path.parent.name != "planit":
            continue
        if any(part in _SKIP for part in path.parts):
            continue
        found.append(path.relative_to(root).as_posix())
    return sorted(set(found))


def duplicate_planit_skill_errors(root: Path) -> list[str]:
    """Fail when more than one distinct on-disk planit/SKILL.md exists."""
    by_inode: dict[tuple[int, int], list[str]] = {}
    for rel in on_disk_planit_skill_paths(root):
        path = root / rel
        if not path.is_file():
            continue
        st = path.stat()
        key = (st.st_dev, st.st_ino)
        by_inode.setdefault(key, []).append(rel)
    if len(by_inode) <= 1:
        return []
    detail = "; ".join(f"{', '.join(rels)}" for rels in by_inode.values())
    return [f"multiple planit SKILL.md files on disk ({detail})"]


def _planit_skill_reference_ok(ref: str) -> bool:
    norm = ref.replace("\\", "/")
    if norm == CANONICAL_PATH or norm.endswith(CANONICAL_PATH):
        return True
    if norm == ".cursor/skills/planit/SKILL.md":
        return True
    if norm.endswith("../planit/SKILL.md"):
        return True
    return False


def _route_scan_paths(root: Path) -> list[str]:
    rels: set[str] = set()
    for prefix in _ROUTE_SCAN_PREFIXES:
        base = root / prefix.rstrip("/")
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".mdc"}:
                continue
            if any(part in _SKIP for part in path.parts):
                continue
            rel = path.relative_to(root).as_posix()
            if any(rel.startswith(ex) for ex in _ROUTE_SCAN_EXCLUDE_PREFIXES):
                continue
            if rel in _ROUTE_IGNORE_FILES:
                continue
            rels.add(rel)
    for name in _ROUTE_SCAN_ROOT_FILES:
        if (root / name).is_file():
            rels.add(name)
    return sorted(rels)


def external_planit_route_errors(root: Path) -> list[str]:
    """Fail when skills or docs route outside the canonical in-repo Planit."""
    errors: list[str] = []
    for rel in _route_scan_paths(root):
        try:
            text = (root / rel).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for marker in _EXTERNAL_PLANIT_MARKERS:
            if marker in text:
                errors.append(f"{rel} references external Planit ({marker})")
        for match in _PLANIT_SKILL_REF.findall(text):
            if not _planit_skill_reference_ok(match):
                errors.append(f"{rel} references non-canonical Planit skill ({match})")
    return errors


def one_owned_errors(root: Path) -> list[str]:
    """Default-closed: exactly one owned Planit skill and no external routes."""
    errors: list[str] = []
    errors.extend(duplicate_planit_skill_errors(root))
    errors.extend(external_planit_route_errors(root))
    canonical = root / CANONICAL_PATH
    if not canonical.is_file():
        errors.append(f"missing canonical Planit skill ({CANONICAL_PATH})")
    return errors


def one_owned_main() -> int:
    """Fitness entry: one owned in-repo Planit (ADR 0046 extension)."""
    root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(root / "tools"))
    from nlc_pipeline import is_hub_repo

    if not is_hub_repo(root):
        print("PLANIT_ONE_OWNED:MET skip (hub-only gate, not hub tree)")
        return 0
    errors = one_owned_errors(root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("PLANIT_ONE_OWNED:NOT_MET")
        return 1
    print("PLANIT_ONE_OWNED:MET")
    return 0


def resolve_root(argv: list[str]) -> Path:
    """Hub tree under test: optional path argv before flags."""
    args = list(argv)
    while args and args[0].startswith("-"):
        flag = args.pop(0)
        if flag in {"--loaded", "--record"} and args:
            args.pop(0)
    if args and not args[0].startswith("-"):
        return Path(args[0]).resolve()
    return Path(__file__).resolve().parents[3]


def main() -> int:
    args = sys.argv[1:]
    root = resolve_root(args)
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from nlc_pipeline import is_hub_repo

    if not is_hub_repo(root):
        print("PLANIT_IDENTITY:MET skip (hub-only gate, not hub tree)")
        return 0
    loaded = CANONICAL_PATH
    if "--loaded" in args:
        loaded = args[args.index("--loaded") + 1]
    errors = prove(root, loaded)
    if "--record" in args and not errors:
        registry = load_registry(root)
        record = {
            "planit_skill_path": registry.get("canonical_path"),
            "planit_skill_sha256": registry.get("content_sha256"),
            "source_tree_sha256": source_tree_hash(root),
        }
        dest = root / EVIDENCE_REL
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print("PLANIT_IDENTITY:RECORDED")
        return 0
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("PLANIT_IDENTITY:NOT_MET")
        return 1
    if "--check-evidence" in args or ("--record" not in args and "--skill-only" not in args):
        evidence = evidence_errors(root, load_registry(root))
        if evidence:
            for item in evidence:
                print(f"VIOLATION {item}")
            print("PLANIT_IDENTITY:NOT_MET")
            return 1
    print("PLANIT_IDENTITY:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
