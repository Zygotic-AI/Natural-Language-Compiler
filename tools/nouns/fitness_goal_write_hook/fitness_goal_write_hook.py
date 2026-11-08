"""ADR 0058: NLC must not register harness hooks as compile enforcement."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOOKS_JSON = Path(".cursor") / "hooks.json"
HOOKS_DIR = Path(".cursor") / "hooks"
_EVENTS = (
    "preToolUse",
    "postToolUse",
    "beforeSubmitPrompt",
    "afterAgentResponse",
    "preCompact",
    "sessionStart",
    "sessionEnd",
)


def nlc_harness_hook_errors(root: Path) -> list[str]:
    errors: list[str] = []
    hooks_path = root / HOOKS_JSON
    if hooks_path.is_file():
        try:
            data = json.loads(hooks_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return [f"{HOOKS_JSON.as_posix()}: invalid json ({exc})"]
        hooks = data.get("hooks") if isinstance(data, dict) else None
        if isinstance(hooks, dict):
            for event in _EVENTS:
                entries = hooks.get(event)
                if isinstance(entries, list) and entries:
                    errors.append(
                        f"{HOOKS_JSON.as_posix()} registers {event} as NLC enforcement"
                    )
            extra = [str(k) for k in hooks if str(k) not in _EVENTS and hooks.get(k)]
            for event in extra:
                errors.append(
                    f"{HOOKS_JSON.as_posix()} registers {event} as NLC enforcement"
                )
        elif hooks:
            errors.append(f"{HOOKS_JSON.as_posix()} has hooks")
    hooks_dir = root / HOOKS_DIR
    if hooks_dir.is_dir():
        for path in sorted(hooks_dir.iterdir()):
            if path.is_file() and path.name.startswith("nlc-"):
                errors.append(
                    f"{path.relative_to(root).as_posix()} is an NLC harness hook script"
                )
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    errors = nlc_harness_hook_errors(root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
