# RCA: tag-time containment graded a stale local release branch

**Date:** 2026-11-11
**Queue id:** RCA-S11
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only.

---

## 1. Error condition

**Observed.** Containment reads the **local** `release/v*` name. [`nlc_release_context.py`](../../tools/nouns/nlc_release_context/nlc_release_context.py) `main_context` runs `git rev-list ${remote}/${base} ^${rel_branch}` with `rel_branch` as `release/v0.7.0` (no `origin/` prefix). Local `release/v0.7.0` was behind `origin/release/v0.7.0`, so `./release` reported `BLOCKED_MAIN_CONTEXT_NOT_CONTAINED` until a fast-forward. The remote line already contained `main`.

**Observed (planner).** When `remote_relation` is `behind`, planner selects `FAST_FORWARD_LOCAL`. That repair exists, but tag-time `./release` graded containment on the stale local ref first and printed NOT_MET as if origin were uncontained.

**Not this record.** Actual squash non-containment on origin (S08/S15).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | `./release` | `BLOCKED_MAIN_CONTEXT_NOT_CONTAINED` while origin was contained |
| 3 | `main_context(..., rel_branch)` | Diffs `origin/main` against **local** `release/v*` |
| 2 | No fetch/ff before grade | Observer uses whatever the worktree branch is |
| 1 | [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) | `main_context` is origin/main vs the **release branch** — meaning the line being shipped, which is origin when a remote exists |
| 0 | Skill resume | Lists branches; tag path skipped a fetch |

**Furthest controllable point:** `main_context` treats the local ref name as the release line even when `origin/release/v*` exists and is ahead.

---

## 3. Impact / scope

False NOT_MET at tag time. Extra fetch/ff ritual. Looks like a containment incident when it is a stale local.

---

## 4. Timeline

| Event | Note |
| --- | --- |
| Origin `release/v0.7.0` | Contained `main` after #74 |
| Local `release/v0.7.0` | Behind origin |
| Tag-time `./release` | Containment NOT_MET until ff-only |

---

## 5. Mechanism on reproduction

**Confirmed from bytes.** `main_context` second rev-list arg is `f"^{rel_branch}"`, not `f"^{remote}/{rel_branch}"`. A behind local includes every origin-only commit in `origin/main ^local`, including merges that *are* on origin’s release line.

---

## 6. The one thing

`main_context` must grade `origin/main` against `origin/release/v*` when that remote-tracking ref exists (or fetch + fast-forward the local line before the grade). A stale local `release/v*` must not be the containment input.

---

## 7. Prevention test

If that ref choice had been in place, a local branch behind origin could not have produced `BLOCKED_MAIN_CONTEXT_NOT_CONTAINED` while `origin/release/v0.7.0` already contained `main`.

---

## 8. Contributing factors

- Planner `FAST_FORWARD_LOCAL` would have fixed the local ref if selected before the containment block. Containment is checked *before* `remote_relation == behind` in `plan_release`.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | In `nlc_release_context.py`, compare `origin/main` to `origin/<release-branch>` when the remote-tracking ref exists; otherwise fetch then grade. Do not use a behind local as the only `^` tip. |
| Owner | hub maintainer |
| Path | `tools/nouns/nlc_release_context/nlc_release_context.py`; optionally reorder planner so FAST_FORWARD_LOCAL precedes containment when relation is behind |
| Verification | A fixture local-behind, origin-contained worktree prints `contained`, not `BLOCKED_MAIN_CONTEXT_NOT_CONTAINED`. |
| Implementation route | not in this record |

---

## 10. Follow-up

If planner order is also wrong (containment before behind), that is the same one thing’s verification, not a second RCA.
