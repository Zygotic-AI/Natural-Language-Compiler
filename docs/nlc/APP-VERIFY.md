# [App repo](../TERMS.md#adopter) [verify](../TERMS.md#verify)

Two stages. One rule ([ADR 0021](../../adrs/0021-verify-fast-and-deep.md)).

1. **Interview done, not compiled yet** — no files under `goals/`, no `domain/**/*.py`. `./nlc verify` checks `.nlc/interview-packet.json` only. `./nlc verify-deep` does not run hub `release-audit.py` and does not write fingerprints. Next step is `/planit`.
2. **Compiled** — `goals/` has files or `domain/` has Python. `./nlc verify` checks fingerprints (`.nlc/verified.json`) plus pipeline blockers. `./nlc verify-deep` runs `.nlc/verify-suite.json` when you added one, then refreshes fingerprints.

**Ship** is separate: `./nlc ship-check` (hub `release-audit.py` plus human `Released-by:`). Prove is not ship.

[Hub](../TERMS.md#hub) specimens use `ci_fitness.py`. Hub MET requires empty `git status --porcelain` (the committed tree). Failures on a human path use [ADR 0018](../../adrs/0018-human-cli-interview-on-gap.md) (problem, what’s wrong, ask, choices, examples).

## Optional: custom fitness command

Create **`.nlc/verify-suite.json`**:

```json
{
  "schema": 1,
  "command": ["python3", "tools/my-adopter-fitness.py"],
  "cwd": "."
}
```

`verify-deep` runs this on a compiled app when the file exists. Use the same command in CI as in `.github/workflows/nlc-verify.yml`.

## CI

`nlc-init` copies `github-workflows-nlc-verify.yml` → `.github/workflows/nlc-verify.yml`.

PRs can run `./nlc verify` before compile: bind-ready packet → pass. After first generate, run `./nlc verify-deep` once and commit **`.nlc/verified.json`** so later PRs compare fingerprints.
