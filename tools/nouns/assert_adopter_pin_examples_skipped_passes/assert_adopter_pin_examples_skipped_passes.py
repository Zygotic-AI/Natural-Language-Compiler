"""Guard: adopter contract walk does not report schemas inside `.nlc`.

Gate (default-closed):
- The pin schema file and the product schema file both exist.
- `schema_files` returns the product schema.
- No returned path has a `.nlc` part.
- `acceptance_blockers` is empty.
- `contract_change_blockers` is empty.
Pass: exit 0. Fail: exit 1.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "adopter-ignores-pin-examples"


def main() -> int:
    root = FIXTURE.resolve()
    pin = root / ".nlc" / "versions" / "0.0.0" / "examples" / "bad" / "input.schema.json"
    product = root / "goals" / "ping" / "input.schema.json"
    if not pin.is_file() or not product.is_file():
        print("ASSERT:FAIL fixture schemas missing")
        return 1
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.fitness_c10.fitness_c10 import schema_files
    from nlc_contract_break_accept import acceptance_blockers
    from nlc_contract_change import contract_change_blockers

    files = schema_files(root)
    leaked = [path for path in files if ".nlc" in path.parts]
    if leaked:
        print("ASSERT:FAIL schema_files returned a path under .nlc")
        for path in leaked:
            print(path)
        return 1
    if product.resolve() not in {path.resolve() for path in files}:
        print("ASSERT:FAIL product schema was not scanned")
        return 1
    blockers = acceptance_blockers(root)
    if blockers:
        print("ASSERT:FAIL acceptance_blockers should be empty")
        for row in blockers:
            print(row)
        return 1
    change = contract_change_blockers(root)
    if change:
        print("ASSERT:FAIL contract_change_blockers should be empty")
        for row in change:
            print(row)
        return 1
    print("ASSERT:PASS adopter pin examples are not contract blockers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
