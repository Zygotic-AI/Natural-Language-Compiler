# RCA: tag-time signature landed in #72 after the ship PR

**Date:** 2026-11-11
**Queue id:** RCA-S16
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Do not fold RCA-S07 into this record.

---

## 1. Error condition

**Observed.** Owner clearsign of `integrity/checker-digest.sha256` (armor committed `bd50f45`, message “chore: ratify checker digest for v0.7.0 tag”) landed via pull request #72 (`cursor/v070-checker-digest-sig-326d` → `release/v0.7.0`, merged 2026-11-10T23:23:41Z as `d6ed697`) **after** ship PR #71 had already merged (22:49:59Z). The human manager was asked to sign after they had already merged a ship PR.

**Observed (ADR).** [ADR 0057](../../adrs/0057-tag-time-checker-digest.md) requires that armor on the tagged commit. v0.6.0 armor (`4ae4fd1`) was on the line **before** the v0.6.0 ship PR.

**Not this record.** Opening #71 before the signature existed (RCA-S07) — that is the missing gate on the offer. This record is the **request/landing order**: signature as a follow-up PR after the ship merge.

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | #72 | Signature PR after ship merge |
| 3 | Skill / session | Requested clearsign as repair after #71 |
| 2 | No HUMAN_DECISION before offer | Signature was not the stop that precedes CREATE_PR |
| 1 | ADR 0057 | Armor is tag-time; the round-trip must complete before the tag candidate is on `main` |
| 0 | [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) | Owner signature is HUMAN_DECISION, not a post-merge repair PR |

**Furthest controllable point:** the owner-signature round-trip is requested after a ship PR to `main` exists, instead of as the HUMAN_DECISION that blocks that offer.

---

## 3. Impact / scope

The operator signed after believing the ship merge was done. Extra PR #72 on the release line. Armor never reached `cc43f3e`.

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-11-10T22:49:59Z | #71 merged (no v0.7.0 armor) |
| After that | Signature requested |
| 2026-11-10T23:23:41Z | #72 merged `d6ed697` / `bd50f45` |

---

## 5. Mechanism on reproduction

**Confirmed.** `git log --oneline -- integrity/checker-digest.sha256.approval.asc`: `bd50f45` is after `4ae4fd1`. `git merge-base --is-ancestor bd50f45 cc43f3e` is false. #72 base is `release/v0.7.0`, not `main`. Planner has no `AWAIT_SIGNATURE` before CREATE_PR.

---

## 6. The one thing

The ADR 0057 owner-signature HUMAN_DECISION must be requested and landed on the release line **before** any ship PR to `main` is offered. After a ship PR merges, the skill must not open a signature PR as the next repair.

---

## 7. Prevention test

If that order had been in place, `bd50f45` would have existed on `release/v0.7.0` before #71, and #72 would not have been the vehicle for tag-time armor. The error condition (signature landing after the ship PR) could not have occurred.

---

## 8. Contributing factors

- S07: offer gate does not check armor (missing refuse). This record is the late request.
- Human-only signature is correct; **when** it is requested is the process.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Planner/skill: HUMAN_DECISION for current checker-digest armor before CREATE_PR to `main`. After a ship PR exists, do not open a signature-only follow-up PR as the next step. |
| Owner | hub maintainer |
| Path | `tools/nouns/release_state/release_state.py`; `.agents/skills/release/SKILL.md` |
| Verification | A fixture unsigned digest selects HUMAN_DECISION, not CREATE_PR. A fixture after a merged ship PR does not select a signature-only PR. |
| Implementation route | not in this record |

---

## 10. Follow-up

S07 remains the offer-without-gate record.
