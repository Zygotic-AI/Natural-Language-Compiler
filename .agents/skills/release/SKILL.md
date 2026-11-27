---
name: release
description: Hub release. Use when the user wants to release, ship, tag, or run ./release.
disable-model-invocation: true
---

# Release (`/release`)

Full steps live in this skill so they are not standing agent context (`AGENTS.md` only points here).

Run the **release goal** and report the result. Do not re-list every check in chat. The goal checks [ADR 0061](../../../adrs/0061-release-in-seven-steps.md) (readiness checklist; first gate names each open milestone issue) then runs the machine steps, gates, and release record. The goal imports the derived mandated-path list (`integrity/mandated-paths.json` from `python3 tools/derive-mandated-paths.py`).

```bash
./goals/hub_release/execute.sh
```

Or the thin entrypoint, which calls the same goal:

```bash
./release validate
./release sign --armor <file>
./release main
./release tag
```

Give the owner only the text between the `RELEASE_SIGN_BLOCK` markers, never commands. Never create armor. Do not move an existing tag, reset `main`, or force-push. Do not write `Released-by:` (adopter ship).

If a command's output contradicts the docs, fix the tool or the docs; never tell the owner to ignore or reinterpret it (`jidoka-ssot-output.md`).
