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
_ROUTE_SCAN_PREFIXES = (
    ".agents/",
    ".cursor/",
    "docs/",
    "integrity/",
    "adrs/",
    "content-types/",
    "agents/",
)
_ROUTE_SCAN_EXCLUDE_PREFIXES = (
    "docs/history/",
    "adrs/history/",
)
_ROUTE_SCAN_ROOT_FILES = ("AGENTS.md", "CHARTER.md", "TODO", "DESCRIBE.md", "README.md")
_ROUTE_IGNORE_FILES = (
    "tools/assert-planit-second-skill-fails.py",
    "tools/assert-planit-external-route-fails.py",
    "tools/assert-planit-other-skill-fails.py",
    "tools/assert-planit-one-owned-landmines.py",
    "tools/nouns/planit_identity/planit_identity.py",
)
_PLANIT_SKILL_REF = re.compile(r"(?<![\w-])([\w./$~-]+/[Pp]lanit/SKILL\.md)")
_EXTERNAL_MARKER_RES = (
    re.compile(r"~/.agents/skills/planit", re.I),
    re.compile(r"\$HOME/.agents/skills/planit", re.I),
    re.compile(r"/home/[\w.-]+/\.agents/skills/planit", re.I),
    re.compile(r"route\s+to\s+global\s+planit", re.I),
    re.compile(r"use\s+global\s+planit", re.I),
)


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


def on_disk_planit_skill_paths(root: Path) -> list[str]:
    """Return repo-relative paths to every planit/SKILL.md on disk (any casing)."""
    found: list[str] = []
    for path in root.rglob("SKILL.md"):
        if path.parent.name.lower() != "planit":
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


def _resolve_in_repo(root: Path, ref: str) -> Path | None:
    """Resolve a skill reference; None when outside the repo root."""
    norm = ref.strip().replace("\\", "/")
    if norm.startswith("~/"):
        return None
    try:
        if norm.startswith("/"):
            resolved = Path(norm).resolve()
        else:
            resolved = (root / norm).resolve()
        resolved.relative_to(root.resolve())
    except (OSError, ValueError):
        return None
    return resolved


def _planit_skill_reference_ok(root: Path, ref: str) -> bool:
    norm = ref.strip().replace("\\", "/")
    if norm.startswith("~/") or "$HOME" in norm or norm.startswith("/home/"):
        return False
    if "zyprompt" in norm.lower():
        return False
    if re.fullmatch(r"\.\./planit/SKILL\.md", norm, flags=re.I):
        return True
    allowed_tails = (CANONICAL_PATH, ".cursor/skills/planit/SKILL.md")
    if not any(norm.lower().endswith(tail.lower()) for tail in allowed_tails):
        return False
    if norm.lower().endswith(CANONICAL_PATH.lower()) and "staging/" in norm.lower():
        return False
    if ".." not in norm and not norm.startswith("/"):
        resolved = _resolve_in_repo(root, norm)
        if resolved is not None:
            canonical = (root / CANONICAL_PATH).resolve()
            if resolved == canonical:
                return True
            cursor = root / ".cursor/skills/planit/SKILL.md"
            if cursor.is_file():
                try:
                    if resolved == cursor.resolve():
                        return True
                except OSError:
                    pass
    canonical = (root / CANONICAL_PATH).resolve()
    if canonical.is_file():
        return True
    return False


def _external_marker_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in _EXTERNAL_MARKER_RES:
        if pattern.search(text):
            hits.append(pattern.pattern)
    return hits


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
        for marker in _external_marker_hits(text):
            errors.append(f"{rel} references external Planit ({marker})")
        for match in _PLANIT_SKILL_REF.findall(text):
            if rel.startswith("docs/rca/"):
                continue
            if not _planit_skill_reference_ok(root, match):
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


def _run_one_owned_landmine(root: Path, rel: str, body: str, expect: tuple[str, ...]) -> int:
    """Write a probe file, run one-owned fitness, require failure with expected text."""
    dest = root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    existed = dest.is_file()
    original = dest.read_text(encoding="utf-8") if existed else None
    proc: subprocess.CompletedProcess[str]
    try:
        if existed:
            dest.write_text(original + "\n" + body, encoding="utf-8")
        else:
            dest.write_text(body, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(root / "tools" / "fitness-planit-one-owned.py")],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        if existed and original is not None:
            dest.write_text(original, encoding="utf-8")
        elif dest.is_file():
            dest.unlink()
            parent = dest.parent
            while parent != root and parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print(f"ASSERT:FAIL probe {rel} must fail one-owned fitness")
        print(combined[-800:])
        return 1
    if not any(fragment in combined for fragment in expect):
        print(f"ASSERT:FAIL probe {rel} missing expected violation ({expect!r})")
        print(combined[-800:])
        return 1
    print(f"ASSERT:PASS probe {rel}")
    return 0


def landmine_second_skill_fails_main() -> int:
    """Landmine: a second planit/SKILL.md must fail one-owned fitness."""
    root = Path(__file__).resolve().parents[3]
    extra = Path("staging/x/Planit/SKILL.md")
    dest = root / extra
    dest.parent.mkdir(parents=True, exist_ok=True)
    proc: subprocess.CompletedProcess[str]
    try:
        dest.write_text("# landmine second planit\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(root / "tools" / "fitness-planit-one-owned.py")],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        if dest.is_file():
            dest.unlink()
        for directory in (
            root / "staging" / "x" / "Planit",
            root / "staging" / "x",
            root / "staging",
        ):
            if directory.is_dir() and directory != root and not any(directory.iterdir()):
                directory.rmdir()
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print("ASSERT:FAIL second planit SKILL.md must fail one-owned fitness")
        print(combined[-800:])
        return 1
    if "multiple planit SKILL.md" not in combined:
        print("ASSERT:FAIL expected duplicate planit violation")
        print(combined[-800:])
        return 1
    print("ASSERT:PASS second planit SKILL.md is refused")
    return 0


def landmine_external_route_fails_main() -> int:
    """Landmine: a ~/.agents/skills/planit route must fail one-owned fitness."""
    root = Path(__file__).resolve().parents[3]
    return _run_one_owned_landmine(
        root,
        ".agents/skills/_landmine_external_planit_route.md",
        "route to `~/.agents/skills/planit`\n",
        ("external Planit", "~/.agents/skills/planit"),
    )


def landmine_one_owned_probes_main() -> int:
    """Landmines for each one-owned spelling class (default-closed)."""
    root = Path(__file__).resolve().parents[3]
    probes: tuple[tuple[str, str, tuple[str, ...]], ...] = (
        (
            ".agents/skills/_landmine_home_route.md",
            "prefer $HOME/.agents/skills/planit for KCR\n",
            ("external Planit", "$HOME"),
        ),
        (
            ".agents/skills/_landmine_abs_home_skill.md",
            "see /home/rpickett/.agents/skills/planit/SKILL.md\n",
            ("non-canonical", "rpickett"),
        ),
        (
            ".agents/skills/_landmine_traversal_skill.md",
            "vendored from ../../../zyprompt/skills/../planit/SKILL.md\n",
            ("non-canonical", "zyprompt"),
        ),
        (
            "docs/rca/_landmine_global_planit_prose.md",
            "DSI Phase 6 instance (route to global Planit)\n",
            ("external Planit", "global"),
        ),
        (
            ".agents/skills/_landmine_case_tilde.md",
            "sync from ~/.agents/skills/Planit\n",
            ("external Planit", "Planit"),
        ),
        (
            ".cursor/rules/_landmine_planit_route.mdc",
            "invoke ~/.agents/skills/planit before planit\n",
            ("external Planit",),
        ),
        (
            "README.md",
            "\n<!-- landmine: route to `~/.agents/skills/planit` -->\n",
            ("external Planit", "README.md"),
        ),
    )
    exit_code = 0
    for rel, body, expect in probes:
        if _run_one_owned_landmine(root, rel, body, expect) != 0:
            exit_code = 1
    return exit_code


def landmine_stale_evidence_fails_main() -> int:
    """Landmine: stale planit-change-evidence must fail --check-evidence."""
    root = Path(__file__).resolve().parents[3]
    evidence = root / EVIDENCE_REL
    if not evidence.is_file():
        print("ASSERT:FAIL missing planit-change-evidence.json")
        return 1
    original = evidence.read_text(encoding="utf-8")
    proc: subprocess.CompletedProcess[str]
    try:
        record = json.loads(original)
        record["source_tree_sha256"] = "0" * 64
        evidence.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        proc = subprocess.run(
            [
                sys.executable,
                str(root / "tools" / "fitness-planit-identity.py"),
                "--skill-only",
                "--loaded",
                CANONICAL_PATH,
                "--check-evidence",
            ],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        evidence.write_text(original, encoding="utf-8")
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print("ASSERT:FAIL stale planit change evidence must fail --check-evidence")
        print(combined[-800:])
        return 1
    if "Planit change evidence does not match the current tree" not in combined:
        print("ASSERT:FAIL expected stale evidence violation")
        print(combined[-800:])
        return 1
    print("ASSERT:PASS stale planit change evidence is refused")
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