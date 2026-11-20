---
name: verify
description: NLC verify — interview packet before compile, fingerprints after. Use /verify when ./nlc verify fails or before release.
disable-model-invocation: true
---

# Verify

Human and CI run **`./nlc verify`**.

- **Not compiled** (no files under `goals/`, no `domain/**/*.py`): pass means the interview packet is bind-ready. Next is `/planit`.
- **Compiled:** pass means fingerprints match `.nlc/verified.json` and pipeline blockers are clear. Refresh with **`./nlc verify-deep`** after generate.
- **Ship** is **`./nlc ship-check`**, not verify-deep.

On fail, stderr is ADR 0018 (problem, What's wrong, ask, options, examples). Follow those lines. Do not treat `Reproduce:` as the human surface.

## Gate

| Criterion | Blocking? | Pass when |
| --------- | --------- | --------- |
| `./nlc verify` | yes | Exit 0 after your fixes |
| Fingerprints | yes after compile | `verify-deep` run when generated files changed |

## Procedure

1. Run **`./nlc`** — read **YOUR QUEUE** (Requirements before Build).
2. Run **`./nlc verify`**. If pass and compile has not started, hand off `/planit`. If pass and compiled, the tree is compile-green (not shipped).
3. On fail — use the printed What's wrong / Option / Example lines. `/interview` if the packet is missing. `/planit` if interview is done. `./nlc verify-deep` only after compiled files exist.
4. **Gate after generate (ADR 0010):** if verify cites a stale `implementation.py` or scoped skill path, run the plan's fitness, then `./nlc maintainer gate-record --artifact <path> --gate-id <id> --command "<cmd>"`.
5. **Rule trace (ADR 0023):** `./nlc maintainer rule-coverage --check` for missing `nlc:rule=` markers; emit via `./nlc maintainer rule-marker --id <rule_id>` on regen, not hand-edited comments.
6. Run **`./nlc verify-deep`** only after compile output exists. Then confirm **`./nlc verify`** is green.

## Done signals

- `./nlc verify` exit 0
- Human knows: packet before compile; fingerprints after; ship is `./nlc ship-check`
