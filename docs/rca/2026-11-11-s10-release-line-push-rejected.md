# RCA: prep committed on local release/v0.7.0; push rejected (recurrence)

**Date:** 2026-11-11
**Queue id:** RCA-S10
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Recurrence of [`2026-10-31-release-line-push-without-pr.md`](2026-10-31-release-line-push-without-pr.md). Do not fold RCA-S09 into this record.

---

## 1. Error condition

**Observed.** After WRITE_RECORD stall, the producer committed “Release v0.7.0” on local `release/v0.7.0` and `git push origin release/v0.7.0` was rejected by GitHub ruleset `25824126` (pull request required; fitness required). Work was replayed on `cursor/v070-release-prep-326d` as pull request #70 (merged 2026-11-10T22:45:32Z).

**Observed (still true).** `goals/hub_release/execute.sh` `PUSH_NEW|PUSH_FAST_FORWARD` still runs `git push -u "${REMOTE}" "${branch}"` of the desired `release/v*` name. [`release_state.py`](../../tools/nouns/release_state/release_state.py) still chooses `PUSH_FAST_FORWARD` when `remote_relation` is `ahead`. [`docs/github-ruleset-release.md`](../github-ruleset-release.md) still says a producer session must not push `release/*`.

**Prior RCA.** 2026-10-31: same class on `release/v0.4.1`. Preventive action in that record was not implemented. This 2026-11-10 push is a new instance of the same process defect.

**Not this record.** The stall that provoked a hand commit (RCA-S09).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | `git push origin release/v0.7.0` | Ruleset reject |
| 3 | Hand commit on `release/v*` | First publication of those commits |
| 2 | Planner PUSH_FAST_FORWARD | Direct push is still the action for local-ahead |
| 1 | 2026-10-31 RCA | Named this; not implemented |
| 0 | Ruleset `25824126` | PR + fitness required before that ref moves |

**Furthest controllable point:** the planner action for “local release branch is ahead of origin” is still a direct push of `release/*`. That is the same furthest point as 2026-10-31.

---

## 3. Impact / scope

Prep could not land on the release line until a work-branch PR (#70). Same extra loop as v0.4.1.

---

## 4. Timeline

| Time | Event |
| --- | --- |
| 2026-10-31 | RCA on PUSH_FAST_FORWARD reject; no planner change |
| 2026-11-10 | Same push class on `release/v0.7.0` rejected |
| 2026-11-10T22:45:32Z | #70 merged into `release/v0.7.0` |

---

## 5. Mechanism on reproduction

**Confirmed.** `git grep -n "git push" goals/hub_release/execute.sh` still matches PUSH_FAST_FORWARD. Ruleset JSON still requires pull_request on `refs/heads/release/*`. 2026-10-31 record §9 action is not in the tree.

---

## 6. The one thing

Implement the 2026-10-31 preventive action: when local `release/v*` is ahead, the planner must land those commits via a non-`release/*` branch and a pull request (with fitness) — not `git push` of `release/v*` as the first time those commits are seen.

---

## 7. Prevention test

If that planner change had been in place after 2026-10-31, the 2026-11-10 `git push origin release/v0.7.0` of a new commit would not have been selected. The recurrence could not have occurred.

---

## 8. Contributing factors

- S09 stall invited a hand commit on the release branch.
- Docs say “do not push”; the planner still does.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Same as 2026-10-31 §9: replace PUSH_FAST_FORWARD of unseen `release/*` commits with work-branch + PR into `release/v*`. |
| Owner | hub maintainer |
| Path | `tools/nouns/release_state/release_state.py`; `goals/hub_release/execute.sh` |
| Verification | A fixture local-ahead release branch selects CREATE_PR (or equivalent) on a non-release head, not `git push origin release/v*`. |
| Implementation route | not in this record |

---

## 10. Follow-up

Cite 2026-10-31; do not close that record by this recurrence alone until the planner changes.
