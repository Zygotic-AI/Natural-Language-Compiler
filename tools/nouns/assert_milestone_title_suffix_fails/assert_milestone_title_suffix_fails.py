"""Landmine ADR 0061: milestone title must end with ' - vX.Y.Z'; zero or many refuse."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.hub_release.hub_release import select_milestones

    zero, err = select_milestones(
        [{"title": "Planit Sharpening - v0.9.0"}, {"title": "Other"}],
        "0.10.0",
    )
    if zero or "zero" not in err or "v0.9.0" not in err:
        print("ASSERT:FAIL expected zero-match refuse that names what it found")
        print(err)
        return 1
    two, err = select_milestones(
        [
            {"title": "Planit Sharpening - v0.10.0"},
            {"title": "Also - v0.10.0"},
        ],
        "0.10.0",
    )
    if two or "more than one" not in err or "Also - v0.10.0" not in err:
        print("ASSERT:FAIL expected more-than-one refuse that names matches")
        print(err)
        return 1
    one, err = select_milestones(
        [
            {"title": "Planit Sharpening - v0.10.0"},
            {"title": "Manifests - v0.11.0"},
        ],
        "0.10.0",
    )
    if err or len(one) != 1 or one[0]["title"] != "Planit Sharpening - v0.10.0":
        print("ASSERT:FAIL expected the v0.10.0 suffix match, not nlc-version.json")
        print(err, one)
        return 1
    print("ASSERT:PASS milestone title suffix is exact; zero and many refuse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
