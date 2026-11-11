# RCA: first WRITE_NOTES stopped on empty Highlights

**Date:** 2026-11-11
**Queue id:** RCA-S12
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only.

---

## 1. Error condition

**Observed.** `./release` action `WRITE_NOTES` wrote `docs/adoption/RELEASE-v0.7.0.md` with `<!-- Replace this block with user-facing summary (required). -->` under `## Highlights`. Gate [`release_notes.py`](../../tools/nouns/release_notes/release_notes.py) `check_notes`: empty Highlights / placeholder → `RELEASE_NOTES:NOT_MET`. `notes_valid` stays false.

**Observed (constants).** `HIGHLIGHTS_PLACEHOLDER = "Replace this block with user-facing summary (required)."` is written by `build_draft` and then refused by `check_notes` on the same bytes.

**Observed (skill).** Release skill: Highlights content is **human-only when invalid**. The draft writer still emits a known-invalid placeholder as if it were a completed repair.

**Not this record.** Checklist instead of `./release` (S02).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | `RELEASE:NOT_MET` | Highlights empty |
| 3 | `build_draft` | Writes the placeholder the checker rejects |
| 2 | Planner WRITE_NOTES | A REPAIR that cannot set `notes_valid` |
| 1 | Skill human-only Highlights | Correct, but after an invalid write |
| 0 | [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) | Repair must change its progress fact; Highlights are HUMAN_DECISION |

**Furthest controllable point:** WRITE_NOTES / `build_draft` emits a draft that `check_notes` immediately fails. Highlights content is required before a notes repair can be MET.

---

## 3. Impact / scope

First `./release` on the line stopped for a placeholder the writer itself inserted. Human edit after refuse, not before write.

---

## 4. Timeline

| Event | Note |
| --- | --- |
| First WRITE_NOTES on v0.7.0 | Placeholder Highlights |
| Notes gate | NOT_MET |
| Later | Human Highlights; notes valid |

---

## 5. Mechanism on reproduction

**Confirmed.** `build_draft` inserts `<!-- {HIGHLIGHTS_PLACEHOLDER} -->`. `check_notes` fails if Highlights empty, contains the placeholder, or starts with `<!--`. WRITE_NOTES progress fact is `notes_valid` (`ACTION_PROGRESS_FACTS`). Writing a failing draft does not set that fact.

---

## 6. The one thing

Highlights content is a HUMAN_DECISION **before** WRITE_NOTES may write a notes file. `build_draft` must not write `HIGHLIGHTS_PLACEHOLDER` as a completed repair. If Highlights are missing, planner returns HUMAN_DECISION, not a draft that `check_notes` is guaranteed to refuse.

---

## 7. Prevention test

If that order had been in place, the first WRITE_NOTES could not have produced an empty-Highlights `RELEASE_NOTES:NOT_MET` from its own placeholder. The gate would have asked for Highlights first.

---

## 8. Contributing factors

- ADR 0060 / install-scope story was already known and belonged in Highlights before `./release`.
- Detection (gate after write) exists; it does not prevent the invalid write.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Planner: missing Highlights → HUMAN_DECISION, not WRITE_NOTES of a placeholder. Remove placeholder emission from `build_draft`, or require Highlights input before write. |
| Owner | hub maintainer |
| Path | `tools/nouns/release_notes/release_notes.py`; `tools/nouns/release_state/release_state.py`; `.agents/skills/release/SKILL.md` |
| Verification | A clean tree with no notes file prints HUMAN_DECISION for Highlights, not a notes file that `check_notes` fails. |
| Implementation route | not in this record |

---

## 10. Follow-up

Do not treat “fill the placeholder faster” as prevention.
