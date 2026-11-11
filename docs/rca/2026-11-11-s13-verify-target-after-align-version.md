# RCA: VERIFY_TARGET after ALIGN_VERSION with 0.6.0 prep surfaces

**Date:** 2026-11-11
**Queue id:** RCA-S13
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Do not fold RCA-S09 into this record.

---

## 1. Error condition

**Observed.** Planner `ALIGN_VERSION` set `integrity/nlc-version.json` to `0.7.0`. The next action `VERIFY_TARGET` runs `python3 tools/nlc.py --project . verify`. That suite includes F1 [`fitness-findings-shipped-tag-sync.py`](../../tools/fitness-findings-shipped-tag-sync.py) (FINDINGS / DESCRIBE current-ship must not contradict identity). FINDINGS / DESCRIBE / `hub-release-record.json` still said `0.6.0`. VERIFY_TARGET failed. The producer then wrote prep surfaces by hand (RCA-S09).

**Observed (order).** [`next_prepare_action`](../../tools/nouns/release_state/release_state.py):

1. `ALIGN_VERSION` if `worktree_file_version != desired`
2. `VERIFY_TARGET` if not `target_verify_met`
3. `PREP` if not `prep_met`
4. `WRITE_RECORD` if record version/branch mismatch

ALIGN_VERSION does not update FINDINGS / DESCRIBE / record (`execute.sh`: `nlc_release_bump.py --align-to` only).

**Not this record.** The subsequent stall from writing those files off-planner (RCA-S09).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | VERIFY_TARGET | `./nlc verify` FAIL on 0.6.0 prose |
| 3 | `next_prepare_action` | Verify immediately after version bump |
| 2 | ALIGN_VERSION | Version file only |
| 1 | F1 | FINDINGS/DESCRIBE must match identity |
| 0 | ADR 0022 / 0049 prepare order | Verify-before-prep on a bumped version is an impossible REPAIR |

**Furthest controllable point:** `VERIFY_TARGET` is selected after `ALIGN_VERSION` and before `PREP` / `WRITE_RECORD`, so verify runs against surfaces that still name the previous ship.

---

## 3. Impact / scope

First post-align `./release` cannot MET. Invites S09 hand writes.

---

## 4. Timeline

| Event | Note |
| --- | --- |
| ALIGN_VERSION | `nlc-version.json` → 0.7.0 |
| VERIFY_TARGET | FAIL (FINDINGS/DESCRIBE/record 0.6.0) |
| Hand prep write | S09 |

---

## 5. Mechanism on reproduction

**Confirmed.** Executor VERIFY_TARGET is `./nlc verify`. F1 reads FINDINGS and DESCRIBE, not FEATURES. ALIGN_VERSION progress fact is `worktree_file_version` only. PREP is the action that runs `nlc_release_prep_surfaces` / release-prep audit.

---

## 6. The one thing

`next_prepare_action` must not select `VERIFY_TARGET` until FINDINGS / DESCRIBE / `hub-release-record.json` match `desired` (PREP / WRITE_RECORD first), or `ALIGN_VERSION` must update those surfaces in the same repair. A version bump followed by verify against old prose is not a progressing REPAIR.

---

## 7. Prevention test

If PREP/WRITE_RECORD (or an ALIGN that writes those surfaces) ran before VERIFY_TARGET, F1 would see 0.7.0 prose and VERIFY_TARGET would not fail solely because ALIGN_VERSION moved the version file.

---

## 8. Contributing factors

- S09 is the hand workaround this order invited.
- FEATURES current-ship is a separate gap (S19).

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Reorder `next_prepare_action` so PREP and WRITE_RECORD (surfaces matching `desired`) precede VERIFY_TARGET after ALIGN_VERSION, or fold those writes into ALIGN_VERSION. |
| Owner | hub maintainer |
| Path | `tools/nouns/release_state/release_state.py` |
| Verification | A fixture version-file 0.7.0 with FINDINGS 0.6.0 selects PREP/WRITE_RECORD, not VERIFY_TARGET. |
| Implementation route | not in this record |

---

## 10. Follow-up

S09 tracks the stall from bypassing WRITE_RECORD, not this order.
