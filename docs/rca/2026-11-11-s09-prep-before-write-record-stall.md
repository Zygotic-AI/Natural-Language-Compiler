# RCA: prep surfaces written before WRITE_RECORD, then stall

**Date:** 2026-11-11
**Queue id:** RCA-S09
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Do not fold RCA-S13 into this record.

---

## 1. Error condition

**Observed.** The producer ran `python3 tools/nlc_release_prep_surfaces.py --write --version 0.7.0 --branch release/v0.7.0` (FINDINGS, DESCRIBE, `integrity/hub-release-record.json`) before planner action `WRITE_RECORD`. The next `./release` selected `WRITE_RECORD` (`python3 tools/nlc_release_record.py`) and stopped `BLOCKED_WRITE_RECORD_STALLED` because the repair produced no fact change.

**Observed (planner).** [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) decision 4: if the same repair recurs with an unchanged progress-fact tuple, the planner returns `BLOCKED_<ACTION>_STALLED`. [`release_state.py`](../../tools/nouns/release_state/release_state.py) implements that from `stalled_action`. `WRITE_RECORD` progress facts are `candidate_record_version` and `candidate_record_branch`.

**Observed (order).** `next_prepare_action`: ALIGN_VERSION → VERIFY_TARGET → PREP → WRITE_RECORD. Side-channel `--write` of the record makes WRITE_RECORD a no-op.

**Not this record.** VERIFY_TARGET failing because surfaces still said 0.6.0 (RCA-S13) — that failure *caused* the hand write.

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | `./release` | `BLOCKED_WRITE_RECORD_STALLED` |
| 3 | `nlc_release_prep_surfaces.py --write` | Wrote the record the planner still owned |
| 2 | Skill / closeout | Allowed a hand prep write when VERIFY_TARGET failed (S13) |
| 1 | Executor stall | Same action, unchanged facts → HUMAN_DECISION stall |
| 0 | ADR 0049 | Repairs belong to the planner; side-channel writes stall |

**Furthest controllable point:** FINDINGS / DESCRIBE / `hub-release-record.json` for the candidate version can be written outside `PREP` / `WRITE_RECORD`.

---

## 3. Impact / scope

`./release` stopped on a stall that looks like “commit by hand.” That hand commit then hit S10 (push rejected).

---

## 4. Timeline

| Event | Note |
| --- | --- |
| ALIGN_VERSION / VERIFY_TARGET fail | Surfaces still 0.6.0 (S13) |
| Hand `nlc_release_prep_surfaces.py --write` | Record already 0.7.0 |
| Next `./release` | WRITE_RECORD stalled |
| Later | Replay on `cursor/v070-release-prep-326d` as #70 |

---

## 5. Mechanism on reproduction

**Confirmed.** Stall code: `NLC_RELEASE_STALLED_ACTION` → `BLOCKED_${stalled_action}_STALLED`. WRITE_RECORD executor: `nlc_release_record.py --version --branch` only. Prep surfaces tool writes the same record path. If version/branch facts already match `desired`, WRITE_RECORD cannot change `ACTION_PROGRESS_FACTS`.

---

## 6. The one thing

Candidate FINDINGS / DESCRIBE / `hub-release-record.json` writes belong only to planner `PREP` and `WRITE_RECORD`. The release skill must forbid `nlc_release_prep_surfaces.py --write` (and equivalent) while `./release` would still select those actions.

---

## 7. Prevention test

If that forbid had been in place, the record would still have been owned by WRITE_RECORD, facts would have changed, and `BLOCKED_WRITE_RECORD_STALLED` could not have occurred from a pre-written record.

---

## 8. Contributing factors

- S13: VERIFY_TARGET before PREP invited the hand write.
- Stall message reads as a human commit, not “let WRITE_RECORD own the file.”

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Skill / executor: do not run `nlc_release_prep_surfaces.py --write` when planner next action is PREP or WRITE_RECORD. Document that stall means the file was written off-planner. |
| Owner | hub maintainer |
| Path | `.agents/skills/release/SKILL.md`; optionally a refuse in `nlc_release_prep_surfaces.py` when a plan cache says WRITE_RECORD |
| Verification | A fixture that pre-writes the record and re-runs WRITE_RECORD is a documented skill refuse, not a silent stall the session “fixes” by committing. |
| Implementation route | not in this record |

---

## 10. Follow-up

S13 remains the order bug that provoked the hand write.
