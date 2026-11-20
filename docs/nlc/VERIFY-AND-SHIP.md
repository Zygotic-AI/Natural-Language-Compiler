# [Verify](../TERMS.md#verify) and [ship](../TERMS.md#ship)

[NLC](../TERMS.md#nlc) separates **[verify](../TERMS.md#verify)** (machine gates on intent-bound artifacts) from **[ship](../TERMS.md#ship)** (human acceptance of release liability).

## [Adopter](../TERMS.md#adopter) commands

| When | Command | Pass means |
| ---- | ------- | ---------- |
| CI / before compile | `./nlc verify` | Interview packet is bind-ready |
| CI / after compile | `./nlc verify` | Fingerprints match `.nlc/verified.json`; pipeline blockers clear |
| After generated files change | `./nlc verify-deep` | Optional app `verify-suite.json`, then refresh fingerprints |
| Promotion | `./nlc ship-check` | Hub `release-audit.py` + human `Released-by:` when required |

On [verify](../TERMS.md#verify) failure: **`/verify`** in your agent — not a ping-pong of scripts.

## Default order

1. Generate one artifact (`/planit`).
2. [Gate](../TERMS.md#gate) that artifact immediately (ADR 0010).
3. **`./nlc verify`** (packet, then fingerprints once compiled). **`./nlc verify-deep`** after generate to write fingerprints.
4. Promotion: **`./nlc ship-check`**.

## [Hub](../TERMS.md#hub) vs [app repo](../TERMS.md#adopter)

- **[Hub](../TERMS.md#hub)** — `./nlc verify` runs `ci_fitness.py`. MET only when `git status --porcelain` is empty: prove grades the committed tree GitHub grades.
- **[App repo](../TERMS.md#adopter)** — packet before compile; fingerprints after. `ship-check` is hub `release-audit.py`. Template `templates/adopter/github-workflows-nlc-verify.yml`.

[Verify](../TERMS.md#verify) PASS is compile-ready. [Ship](../TERMS.md#ship) needs human `Released-by:` on `CONFIRM.md` when your class requires it.

## Layers (ADR cross-walk)

| Layer | What | Tool |
| ----- | ---- | ---- |
| Compile | Per-artifact [gate](../TERMS.md#gate) + tree fitness | [ADR](../TERMS.md#adr) 0010, `gate-record`, [planit](../TERMS.md#planit) 6.5 |
| [Verify](../TERMS.md#verify) | Fingerprints + policy blockers | `./nlc verify` |
| [Verify-deep](../TERMS.md#verify-deep) | Full suite + produce / [change adversarial](../TERMS.md#change-adversarial) | `./nlc verify-deep`, `.nlc/produce-package.json` (hub) or `change-adversarial.json` + produce (app) |
| [Ship](../TERMS.md#ship) | Human release liability | `./nlc ship-check`, `Released-by:` |

Compile [MET](../TERMS.md#met) does not imply [ship](../TERMS.md#ship). See [`HUMAN-JUDGMENT-GATES.md`](HUMAN-JUDGMENT-GATES.md).
