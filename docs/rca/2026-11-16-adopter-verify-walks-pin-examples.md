# RCA — 2026-11-16-adopter-verify-walks-pin-examples

## Verdict

**Result:** PASS (remediation applied 2026-11-16)

**Evidence:** At record time, `node metaprompts/scripts/validate-rca-record.mjs` (zyprompt) on this file → exit 0.

**The one thing:** `schema_files` in `fitness_c10.py` must skip `.nlc` so adopter verify cannot fail on vendored examples.

**Next:** none. Applied: `schema_files` skips `.nlc`. Guard: `tools/assert-adopter-pin-examples-skipped-passes.py`.

---

## 1. Error condition

error_condition: An adopter `./nlc verify` exits 1 on hub example schemas vendored under `.nlc/versions/0.7.0/examples/`. Those schemas are designed-fail specimens for the hub suite. They are not the product’s contracts. Adopter verify is supposed to be the product tree, not the hub suite.

Evidence (observed, 2026-11-16):

- Adopter `upgrade-your-prompt`. `./nlc verify` printed `Verify failed.` and `Reproduce: ./nlc verify --project <adopter>`, then exited 1. That text is `emit_verify_fail` on the non-hub path (`cmd_verify` runs `ci_fitness.py` only when `is_hub_repo` is true).
- Five of the lines were `breaking contract` for paths under `.nlc/versions/0.7.0/examples/`:
  - `examples/version-bump-no-adr/goals/record-bank-payment/input.schema.json` (version:2)
  - `examples/verify-breaking-accept/domain/invoice/schemas/verbs.schema.json` (breaking:currency)
  - `examples/breaking-no-adr/domain/invoice/schemas/verbs.schema.json` (breaking:currency)
  - `examples/c10-changed-out-of-scope/goals/bad/input.schema.json` (breaking:legacy_field)
  - the same file (version:2)
- Reproduced on the installed pin (`tools/nouns/fitness_c10/fitness_c10.py` and `tools/nouns/contract_break_accept/contract_break_accept.py` loaded from `.nlc/versions/0.7.0`): `schema_files(adopter)` returned 471 schemas, all under `.nlc`. `acceptance_blockers(adopter)` returned those same five events. The pin’s `SKIP_DIR_NAMES` is `.git`, `node_modules`, `dist`, `__pycache__`, `.venv`, `venv`. `.nlc` is not in the set.
- `is_hub_repo(adopter)` is false (`tools/nlc.py` and `integrity/nlc-install-hashes.json` are absent at the product root). `is_hub_repo(.nlc/versions/0.7.0)` is true. The pin is a full hub copy, examples included. The adopter has `adrs/*.md`, so `fitness-c10.py`’s own `scan_one` exits 0 (it reports a version break only when the tree has no ADR). `acceptance_blockers` still demands a manager acceptance row for every `breaking_contract_events` hit.
- The same skip set is in this repo’s `tools/nouns/fitness_c10/fitness_c10.py`. This release line still walks `.nlc`.
- The same verify also printed three adopter lines that are not the examples error: `New requirements — what you're building` (that run had no `goals/` or `domain/`; the tree now has both, so that line does not reproduce), `UC4 rule runner: missing .nlc/rule-ir.snapshot.json` (the product snapshot, because `rules/adopted.json` exists; `_hub_skip` skips this on a hub), and `no fingerprint record — run ./nlc verify-deep once` (`iter_verify_paths` already skips `.nlc`). A later call of each `verify_fast` blocker on the current tree still returns only the five example acceptances from `contract_change_blockers`, plus the snapshot, a gate-record line for an edited skill, and the missing fingerprint. Only the five acceptances name `examples/`.

## 2. Impact / scope

Scope: this hub, and every adopter install whose pin contains `examples/` and whose product tree has goals or domain (so `contract_change_applies` is true).

`./nlc verify` on that adopter cannot pass while the pin holds designed-fail schemas and the product has no acceptance rows for them. Adding those rows would record hub fixtures as the product’s breaking contracts.

Severity: moderate. One adopter verify failed. The same walker is on the unreleased line, so the next install of this hub will do it again until the skip changes.

## 3. Timeline

- Install copies a full hub, including `examples/`, into `.nlc/versions/<ver>`.
- Adopter `./nlc verify` takes the non-hub branch and calls `verify_fast` → `contract_change_blockers`.
- That function returns `[]` on a hub. On this adopter it runs `fitness-c10.py` and `fitness-c21.py` against the product root, then `acceptance_blockers`.
- `breaking_contract_events` calls `schema_files`, which `rglob`s `*.json` and does not skip `.nlc`. The five specimen schemas become acceptance blockers.
- `fitness-c21.py` reads only `CONFIRM.md` / `PROPOSAL.md` at the scan root. It does not walk nested example trees. It did not fail.
- The named `hub_only_fitness` list in `integrity/releasable-gates.json` (48 scripts, same list on the pin and on this line) is consulted only inside `ci_fitness` when that suite runs `fitness-*.py` against `examples/invoice-correct`. Adopter `./nlc verify` never starts `ci_fitness`. Those 48 scripts are not what failed, and they are not running on the install.

## 4. Root cause — one thing

one_thing: schema_files in fitness_c10.py must skip .nlc so adopter verify cannot fail on vendored examples

`schema_files` is the walk. `acceptance_blockers` only reports what that walk returns. Fingerprint verify already refuses to descend into `.nlc` (`SKIP_DIR_NAMES` in `tools/nouns/verify/verify.py` includes `.nlc`). The contract walk does not. Until it does, a pin that contains `examples/breaking-no-adr` (and the other designed-fail schemas) is a product breaking contract.

The 48 `hub_only_fitness` names are not this walk. Skipping them inside the hub suite does not stop adopter verify.

## 4b. System layer classification

| Layer | Implicated? | Evidence | Recommended control (summary) |
| ----- | ----------- | -------- | ----------------------------- |
| L0 Symptom | N | The five lines name real schema files and real version or field breaks. The message is the walker’s output. Rewriting the wording would still fail the adopter. | none — do not special-case the example directory names in the message |
| L1 Local system | Y | `cmd_verify` runs `verify_fast` because the adopter is not a hub. `contract_change_blockers` then calls `schema_files`, whose skip set omits `.nlc`. All 471 schemas and all 5 acceptance blockers are under the pin. | `schema_files` skips `.nlc`. A breaking schema only under the pin cannot become an acceptance blocker. |
| L2 Meta-system | N | The call path is `./nlc verify` → `verify_fast` → `contract_change_blockers` → `acceptance_blockers` → `schema_files`. No skill, planit phase, or AWL inspector is on that path. Planit on the adopter ran the compiler and reported the failure. `hub_only_fitness` is an L1 list used only by `ci_fitness`, which this command does not start. | none — the missing skip is in the compiler walker, not in a skill or a plan gate |

## 5. Prevention test

If `schema_files` skipped `.nlc` the way fingerprint verify does, `acceptance_blockers` on an adopter whose pin contains `examples/breaking-no-adr` would not list those schemas. `./nlc verify` would not fail for them.

```
prevention_test:
cmd: python3 tools/assert-adopter-pin-examples-skipped-passes.py
```

The guard is `tools/assert-adopter-pin-examples-skipped-passes.py`, wired from hub fitness. It exits 1 when `schema_files` returns a path with a `.nlc` part. It exits 0 when the product schema is scanned and the pin schema is not an acceptance blocker.

## 6. Poke-yoke (mandatory — apex)

| Field | Value |
|-------|-------|
| poke_yoke | `schema_files` in `tools/nouns/fitness_c10/fitness_c10.py` refuses to descend into `.nlc`, using the same directory name `tools/nouns/verify/verify.py` already skips. A schema whose path contains `.nlc` cannot be returned, so `breaking_contract_events` and `acceptance_blockers` cannot emit it. Adopter verify cannot fail on vendored examples. |
| on_trip | `remediate:hub` — add `.nlc` to `SKIP_DIR_NAMES` in `tools/nouns/fitness_c10/fitness_c10.py`, then re-run `./nlc verify` in the adopter. Do not add manager acceptance rows for the pin’s example schemas. |
| guarantee | After this control is applied, the five specimen schemas under `.nlc/versions/*/examples/` cannot be acceptance blockers on an adopter. A product schema outside `.nlc` is still reported. |

## 7. Contributing factors

- The install pin is a full hub, so `examples/` is on disk inside the product tree even though `is_hub_repo` of the product root is false.
- `fitness-c10.py` still walks those schemas on an adopter. It exits 0 when the product has any ADR, because `scan_one` suppresses the version-break report in that case. The failure the operator sees is `acceptance_blockers`, which does not suppress them.
- `tools/nouns/fitness_schema_identity/fitness_schema_identity.py` uses the same skip set and would also see pin schemas, but adopter `verify_fast` does not call it. It is not part of this failure.
- The other lines in the captured verify (`New requirements`, the UC4 snapshot, the fingerprint) are adopter checks. The snapshot path contains `.nlc/` because that is where the product rule snapshot is stored. Fingerprint enumeration already skips the pin.

## 8. Recommended preventive actions

status: applied

### 8.1 Local system (L1)

| Field | Value |
|-------|-------|
| layer | L1 |
| status | applied |
| Owner | hub verifier |
| Path / artifact | `tools/nouns/fitness_c10/fitness_c10.py` `SKIP_DIR_NAMES`; guard `tools/assert-adopter-pin-examples-skipped-passes.py`; fixture `examples/adopter-ignores-pin-examples/` |
| poke_yoke | `schema_files` skips `.nlc` only. The guard checks path parts, not the `rel()` string. It exits 1 if a returned path has a `.nlc` part, if the product schema was not scanned, or if `acceptance_blockers` or `contract_change_blockers` is non-empty. |
| on_trip | `remediate:hub` — applied. `.nlc` is in `SKIP_DIR_NAMES`. The guard is wired from `tools/nouns/ci_fitness/ci_fitness.py`. Do not record acceptance for pin examples. |
| guarantee | Adopter verify cannot fail because a hub example schema is inside `.nlc/versions/`. Product schemas outside `.nlc` still block when they are breaking and unaccepted. |
| Verification command | `cmd: python3 tools/assert-adopter-pin-examples-skipped-passes.py` |
| Apply via | applied 2026-11-16 |

## 9. Follow-up

Detection only, after the poke-yoke above. Not a substitute.

- Already-pinned `.nlc/versions/0.7.0` trees keep the old walker until a hub that contains the skip is installed. The apply run does not rewrite those pins.
- Do not treat the 48 `hub_only_fitness` scripts as the leak. Adopter verify does not execute them. Do not add the example paths to the product’s contract-break acceptance record.
