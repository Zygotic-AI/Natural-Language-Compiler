# [ADR](../docs/TERMS.md#adr) 0021 — [Verify](../docs/TERMS.md#verify) fast (fingerprints) and [verify-deep](../docs/TERMS.md#verify-deep) (full gates)

- Status: Accepted
- Date: 2026-11-20
- Revision: 2
- Deciders: Human manager
- Class: F (product UX)
- Version class of this change: **patch** (wrong client prove before compile; no new requirement)

## Context

[ADR](../docs/TERMS.md#adr) 0020 splits human shell from agent workflows. **[Verify](../docs/TERMS.md#verify)** is the exception: CI and release pipelines need a **machine true/false** without inference. Revision 1 made client `verify-deep` run hub `release-audit.py` and treated missing `goals/` / `domain/` as unfinished interview. A bind-ready app that had not compiled yet failed prove for folders compile has not written, and printed `Reproduce:` instead of [ADR 0018](0018-human-cli-interview-on-gap.md).

## Decision

1. **Human and CI command:** `./nlc verify`. Exit **0** = pass, **non-zero** = fail.

2. **Compiled** means the app has compile output: a non-empty `goals/` or any `domain/**/*.py`. Empty dirs from `nlc-init` do not count.

3. **Client, not compiled:** `./nlc verify` checks the interview packet only (`.nlc/interview-packet.json`, bind-ready schema). No fingerprints. `./nlc verify-deep` does not run hub `release-audit.py` and does not write `.nlc/verified.json`. Next step is `/planit` generate.

4. **Client, compiled:** `./nlc verify` compares fingerprints in `.nlc/verified.json` plus pipeline blockers. `./nlc verify-deep` runs `.nlc/verify-suite.json` when that file exists, then rewrites fingerprints. It does **not** default to hub `release-audit.py`.

5. **Client ship:** `./nlc ship-check` runs hub `release-audit.py`. Prove is not ship.

6. **Hub:** `./nlc verify` runs `tools/ci_fitness.py`. `./nlc verify-deep` runs the hub **`release`** profile, then the content-tree stamp. Unchanged.

7. **On failure:** [ADR 0018](0018-human-cli-interview-on-gap.md) shape (`emit_gap`): problem, what’s wrong, ask, choices, copy-paste examples. Machine token last. `Reproduce:` is not the human surface.

8. **`prove`:** Removed from the human CLI. [PLANIT](../docs/TERMS.md#planit) step 7 still means “[verify](../docs/TERMS.md#verify)” internally.

9. **Agent skill `/verify`:** Uses the same stage rule. Runs `verify-deep` only after compiled files exist.

## Consequences

- [`tools/nlc_verify.py`](../tools/nlc_verify.py), [`docs/nlc/APP-VERIFY.md`](../docs/nlc/APP-VERIFY.md), [`.agents/skills/verify/SKILL.md`](../.agents/skills/verify/SKILL.md), [`.agents/skills/planit/SKILL.md`](../.agents/skills/planit/SKILL.md), [`.agents/skills/interview/SKILL.md`](../.agents/skills/interview/SKILL.md).
- Menu: missing packet → `/interview`. Bind-ready, not compiled → `/planit`. Compiled, fingerprints stale → `./nlc verify-deep`.

## Rejected

- Defaulting client `verify-deep` to hub `release-audit.py`.
- Treating missing `goals/` / `domain/` as unfinished interview when the packet is bind-ready.
- `Reproduce:` as the human fail surface.
- Fast [verify](../docs/TERMS.md#verify) re-running full `ci_fitness.py` on an app repo.
