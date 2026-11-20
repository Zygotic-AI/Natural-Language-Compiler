# RCA: client verify fail text shipped without the five-part human shape

**Date:** 2026-11-20
**Queue id:** RCA-ADR-0018-verify-fail-shape
**Status:** closed (record + packet; preventive already on this branch)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** How published `./nlc verify` on an adopter pin printed two labels and `Reproduce:` instead of ADR 0018 (five-part human fail: problem, What's wrong, ask, options, examples). Do not fold the stage rule (packet before compile) into a second root. Do not fold `docs/rca/2026-11-16-adopter-verify-walks-pin-examples.md`.

---

## 1. Error condition

**Observed.** On adopter `upgrade-your-prompt` pinned to hub tag `v0.8.0`, `./nlc verify` printed:

```text
New requirements — what you're building
no fingerprint record — run ./nlc verify-deep once
Reproduce: ./nlc verify
```

That is not [ADR 0018](../../adrs/0018-human-cli-interview-on-gap.md): problem, What's wrong, ask, remediation choices, copy-paste next step.

**Observed (tag bytes).** At `v0.8.0`, `emit_verify_fail` in `tools/nouns/verify/verify.py` printed `Verify failed.`, the raw reason strings, then `Reproduce: ./nlc verify --project …`. It did not call `emit_gap`.

**Observed (gates at that tag).** `fitness_interview_gap_shape` required `emit_gap` on `tools/nlc.py`, `tools/nlc_cli_help.py`, pack export/install. It did **not** list `tools/nlc_verify.py`. `assert_interview_packet_fails` checked that a missing packet is a blocker. It did **not** capture stderr from `emit_verify_fail` or require `What's wrong:` / `Option:` / `Example:`.

**Not this record.** Empty `goals/` treated as unfinished interview (stage rule, ADR 0021 revision 2, already on this branch). Pin example schemas under `.nlc/` (2026-11-16 RCA).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | Adopter `./nlc verify` (pin `v0.8.0`) | Two labels + `Reproduce:` |
| 4 | `emit_verify_fail` | `Verify failed.` + raw reasons + `Reproduce:` |
| 3 | `tools/nlc_verify.py` | Thin `from nouns.verify import *`. Fitness `read_tool` follows this to the noun. |
| 2 | `fitness_interview_gap_shape` | ADR 0018 binder. `EMIT_GAP_MODULES` omitted the verify printer. Hub fitness MET. |
| 1 | `assert_interview_packet_fails` | UC1 packet landmine. Did not assert fail **shape**. |
| 0 | Published skills (`planit`, `verify`, `interview`) | Told the session to run verify. Did not emit the CLI text. |

**Furthest controllable point:** a tag can ship an adopter verify fail printer that is not `emit_gap` because the ADR 0018 fitness list and landmine do not cover that printer.

---

## 3. Impact / scope

Every adopter on pin `v0.8.0` sees `Reproduce:` as the human surface when `./nlc verify` fails. The five-part ask does not appear. Skills cannot repair stdout they do not print.

---

## 4. Timeline

| Event | Note |
| --- | --- |
| 2026-09-20 | ADR 0018 Accepted (five-part human fail). |
| Tag `v0.8.0` | `emit_verify_fail` is Reproduce-first. Fitness list omits `nlc_verify.py`. Packet landmine does not check shape. |
| Client prove on `upgrade-your-prompt` | Two labels + `Reproduce: ./nlc verify`. |
| This branch `204c120` | `emit_verify_fail` calls `emit_gap`. Fitness list includes `tools/nlc_verify.py`. Landmine asserts `What's wrong:` / `Option:` / `Example:` and refuses a `Reproduce:` lead. |

---

## 5. Mechanism on reproduction

**Confirmed.** `git show v0.8.0:tools/nouns/verify/verify.py` — `emit_verify_fail` prints `Verify failed.` and `Reproduce:`. `git show v0.8.0:tools/nouns/fitness_interview_gap_shape/fitness_interview_gap_shape.py` — `EMIT_GAP_MODULES` has no `nlc_verify.py`. `git show v0.8.0:tools/nouns/assert_interview_packet_fails/assert_interview_packet_fails.py` — no stderr shape check. `read_tool` concatenates adapter + noun, so listing `tools/nlc_verify.py` is how fitness sees `emit_gap` in the noun.

---

## 6. The one thing

The ADR 0018 fitness binder must include the adopter verify fail printer (`tools/nlc_verify.py` → `nouns/verify`), and a landmine must run `emit_verify_fail` and refuse output that lacks `What's wrong:` / `Option:` / `Example:` or that leads with `Reproduce:`.

---

## 7. Prevention test

If that binder and landmine had been in place, `v0.8.0` could not have been tagged while `emit_verify_fail` printed `Verify failed.` / `Reproduce:`. Fitness would have been NOT_MET; the landmine would have been ASSERT:FAIL.

---

## 8. Contributing factors

- Published skills did not restate the five-part shape. They do not print `./nlc verify` stderr.
- Adopter prove also mixed fingerprints and hub `release-audit` (stage rule). Separate defect. Already remediated on this branch.
- `tools/nlc_verify.py` is a star-import wrapper. A source scan of the adapter bytes alone would miss `emit_gap` in the noun. `read_tool` already follows the import.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Bind `emit_verify_fail` to `emit_gap`. List `tools/nlc_verify.py` in `fitness_interview_gap_shape`. Landmine: captured stderr from `emit_verify_fail` must contain `What's wrong:`, `Option:`, `Example:`, and must not lead with `Reproduce:`. |
| Owner | hub maintainer |
| Path | `tools/nouns/verify/verify.py`; `tools/nouns/fitness_interview_gap_shape/fitness_interview_gap_shape.py`; `tools/nouns/assert_interview_packet_fails/assert_interview_packet_fails.py` |
| Verification | `python3 tools/assert-interview-packet-fails.py` → `ASSERT:PASS`. `python3 tools/fitness-interview-gap-shape.py` → `RESULT:MET`. |
| Implementation route | Already landed on this branch at `204c120`. New TODO row cites that land; do not re-implement. |

---

## 10. Follow-up

Do not treat skill copy alone as prevention of the next Reproduce-first printer. Detection: keep the landmine on the printer, not on skill markdown.
