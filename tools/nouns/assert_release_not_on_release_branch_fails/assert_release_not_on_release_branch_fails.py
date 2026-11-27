"""Landmine ADR 0061: a change branch is refused and named."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.hub_release.hub_release import check_item_1, parse_release_version

    version, err = parse_release_version("cursor/adr-scope-release-goal-5ef0")
    if version is not None or not err:
        print("ASSERT:FAIL expected refuse on change branch")
        return 1
    lines = check_item_1(version, err)
    joined = " ".join(lines)
    if "cursor/adr-scope-release-goal-5ef0" not in joined:
        print("ASSERT:FAIL expected named branch")
        print(joined)
        return 1
    if "release/vX.Y.Z" not in joined:
        print("ASSERT:FAIL expected release/vX.Y.Z reminder")
        print(joined)
        return 1
    version, err = parse_release_version("HEAD")
    lines = check_item_1(version, err)
    if "HEAD" not in " ".join(lines):
        print("ASSERT:FAIL expected detached HEAD named")
        return 1
    version, err = parse_release_version("release/v0.10.0")
    if version != "0.10.0" or err:
        print("ASSERT:FAIL expected 0.10.0 from release/v0.10.0")
        return 1
    print("ASSERT:PASS change branch is refused and named")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
