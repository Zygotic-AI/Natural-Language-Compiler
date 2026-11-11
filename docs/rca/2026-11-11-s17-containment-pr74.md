# RCA: #74 existed only to contain the #71 squash

**Date:** 2026-11-11
**Queue id:** RCA-S17
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Do not fold RCA-S03, S08, or S15 into this record.

---

## 1. Error condition

**Observed.** Branch `cursor/v070-contain-main-326d` / pull request #74 merged `origin/main` into `release/v0.7.0` with ours on digest armor so #73 could merge. Title: “Merge main into release/v0.7.0 (keep v0.7.0 digest armor).” Merged 2026-11-10T23:34:34Z as `d188058`. That PR does not exist in the v0.6.0 ship shape (start-release → one prep PR → one merge-commit to `main`).

**Observed (planner).** [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) allowlisted automatic mutations do not include merge of `main` into the release line. `CREATE_PR` is to `BASE_BRANCH` (`main`), not a containment PR. Producing #74 made containment-after-squash look like a normal ship step.

**Not this record.** The squash object (S15). Opening #73 early (S08). Offer without merge-method lock (S03).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | #74 | Extra containment PR |
| 3 | Session repair | Merge `main` into `release/v*` with ours on armor |
| 2 | Planner | No CREATE_CONTAINMENT_PR; squash is `not_contained` / not taggable |
| 1 | ADR 0049 | Automatic merge forbidden; HUMAN_DECISION when context is not contained |
| 0 | Ship shape | v0.6.0 had no such PR; this session normalized one |

**Furthest controllable point:** after a squash on `main`, the process treats “open a containment PR” as the next ship step instead of HUMAN_DECISION / INVALID_MERGED that the squash is not a taggable ship.

---

## 3. Impact / scope

Extra merge click, extra conflict resolution, extra “merge 74 then 73” instruction. Containment-after-squash became a ritual.

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-11-10T22:49:59Z | #71 squash |
| 2026-11-10T23:23:41Z | #72 signature |
| 2026-11-10T23:34:34Z | #74 containment merge `d188058` |
| 2026-11-10T23:39:01Z | #73 merge commit tagged |

---

## 5. Mechanism on reproduction

**Confirmed.** #74 base `release/v0.7.0`, head `cursor/v070-contain-main-326d`. `2e868b1` parents are `cc43f3e` and `d188058` — the second parent is this containment merge. Planner `ACTION_KINDS` has no containment-merge repair. ADR 0049: “Automatic merge … forbidden.”

---

## 6. The one thing

A squash of a ship PR on `main` must be a terminal invalid ship (planner HUMAN_DECISION / INVALID_MERGED: do not tag; do not invent a containment PR). The next legal step is a new merge-commit ship on a contained line, not “merge main into release/v* so the conflicting PR can land.”

---

## 7. Prevention test

If that stop had been in place, #74 would not have been a ship-session repair. The error condition (an extra containment PR required to finish the cut) could not have been produced as a normal next step.

---

## 8. Contributing factors

- S15 created `not_contained`.
- S08 offered #73 anyway, which then needed #74.
- Detection (`main_context`) is correct; using it as a merge recipe is the defect.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Skill/planner: `BLOCKED_MAIN_CONTEXT_NOT_CONTAINED` after a squash ship merge is HUMAN_DECISION (do not tag; do not merge `main` into `release/v*` as a producer repair). Document that #74-shaped PRs are not a ship step. |
| Owner | hub maintainer |
| Path | `.agents/skills/release/SKILL.md`; `tools/nouns/release_state/release_state.py` fixes text |
| Verification | A fixture squash on `main` does not select a containment PR; it prints HUMAN_DECISION. |
| Implementation route | not in this record |

---

## 10. Follow-up

S03/S08/S15 remain the earlier links. This record is the extra PR as a ship step.
