# RCA: second ship PR opened before origin/main was contained

**Date:** 2026-11-11
**Queue id:** RCA-S08
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Do not fold RCA-S05 or RCA-S17 into this record.

---

## 1. Error condition

**Observed.** After #71 squash `cc43f3e`, `origin/main` had a non-merge commit not on `release/v0.7.0`. The producer opened pull request #73 (`release/v0.7.0` → `main`) before merging `origin/main` into the release line. #73 was `CONFLICTING`. Containment ([`nlc_release_context.py`](../../tools/nouns/nlc_release_context/nlc_release_context.py)) reports `not_contained` when a commit on main is not a merge (`len(fields) < 3` → “is not a merge commit”).

**Observed (planner).** [`release_state.py`](../../tools/nouns/release_state/release_state.py) returns `BLOCKED_MAIN_CONTEXT_NOT_CONTAINED` before `CREATE_PR`. #73 was therefore not opened by `./release` CREATE_PR after that refuse. It was opened by the producer offer path ([`.agents/skills/release/SKILL.md`](../../.agents/skills/release/SKILL.md) step 5b `pr-offer-gate.py`), which does not call `main_context`.

**Not this record.** Merge-count while conflicting (RCA-S05). Existence of #74 (RCA-S17).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | #73 | Opened to `main` while not contained |
| 3 | pr-offer-gate / skill 5b | `gh pr create` without `main_context == contained` |
| 2 | Planner | Would have blocked CREATE_PR |
| 1 | [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) | `main_context` is a required enum; squash is `not_contained` |
| 0 | Skill “only pr-offer-gate may create” | That command is not bound to containment |

**Furthest controllable point:** the only allowed `gh pr create` (`pr-offer-gate.py`) can offer `release/v*` → `main` while `main_context` is `not_contained`.

---

## 3. Impact / scope

#73 could not merge until #74 contained main. Extra conflict, extra PR, extra human question.

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-11-10T22:49:59Z | #71 squash `cc43f3e` on `main` |
| After that | #73 opened; CONFLICTING |
| 2026-11-10T23:34:34Z | #74 merged into `release/v0.7.0` |
| 2026-11-10T23:39:01Z | #73 merged |

---

## 5. Mechanism on reproduction

**Confirmed.** `main_context` on a squash: `rev-list --parents -n 1 cc43f3e` has two fields (commit + one parent) → not a merge. Planner `if main_context != "contained": BLOCKED_MAIN_CONTEXT_*` sits above CREATE_PR. `pr-offer-gate.py` has no `nlc_release_context` import.

---

## 6. The one thing

`python3 tools/pr-offer-gate.py` (and any CREATE_PR path) must refuse a `release/v*` → `main` offer unless `nlc_release_context.main_context` is `contained`. A second ship PR while main holds a squash is not an offer.

---

## 7. Prevention test

If that refuse had been in place, #73 could not have opened until after containment. The error condition (ship PR before contained) could not have occurred.

---

## 8. Contributing factors

- S15: squash made `not_contained`.
- S17: #74 was the containment repair invented after this offer.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | `pr-offer-gate.py` must call `main_context` and refuse `release/v*` → `main` unless status is `contained`. |
| Owner | hub maintainer |
| Path | `tools/pr-offer-gate.py`; `.agents/skills/release/SKILL.md` step 5b |
| Verification | A fixture with a squash on `main` not on the release line prints `PR_OFFER_GATE:NOT_MET` and does not create a PR. |
| Implementation route | not in this record |

---

## 10. Follow-up

S05 (count) and S17 (extra PR) remain separate.
