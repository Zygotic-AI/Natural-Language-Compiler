# RCA: ship PR to main offered with squash still legal

**Date:** 2026-11-11
**Queue id:** RCA-S03
**Status:** open (RCA only)
**Skill:** Planit RCA standard.

**Scope (manifest):** Analysis only. Do not fold RCA-S15 into this record.

---

## 1. Error condition

**Observed.** Pull request #71 (`release/v0.7.0` → `main`) was offered as the ship merge. Body: “Merge this PR into `main`. After merge, `./release` tags **v0.7.0** on that merge commit.” It did not say squash is invalid. GitHub repo settings: `allow_squash_merge=true`, `allow_merge_commit=true`, `allow_rebase_merge=true`.

**Observed.** `goals/hub_release/execute.sh` `CREATE_PR` runs `gh pr create` directly, not `python3 tools/pr-offer-gate.py`. Title/body are `Release v${desired}` only.

**Contrast.** `v0.6.0` ship PR #63 merged as `3e098b2` with two parents (`Merge pull request #63`). PR #73 later used the title “merge commit — do not squash”.

**Not this record.** The squash object `cc43f3e` (RCA-S15). Tag-next sentence after merge (RCA-S04).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | PR #71 offer | No hard stop that squash cannot be tagged |
| 3 | GitHub repo merge methods | Squash is legal on `main` |
| 2 | `CREATE_PR` / offer body | Mentions “merge commit” as where the tag goes; does not lock the method |
| 1 | [ADR 0044](../../adrs/0044-hub-release-production-trunk.md) | Tag is on a merge commit |
| 0 | No ruleset on `main` for head `release/v*` | Merge method is memory |

**Furthest controllable point:** a `release/v*` → `main` pull request can be merged with squash because GitHub allows it and the offer/planner does not lock merge-commit-only.

---

## 3. Impact / scope

Human manager could squash. That produced RCA-S15 and then S17. v0.6.0 used a two-parent merge without a repo lock either — luck, not a gate.

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-11-08T21:53:01Z | #63 merge commit `3e098b2` (two parents) tagged as `v0.6.0` |
| 2026-11-10T22:49:59Z | #71 merged as squash `cc43f3e` (one parent) |

---

## 5. Mechanism on reproduction

**Confirmed.** `gh api repos/Zygotic-AI/Natural-Language-Compiler --jq .allow_squash_merge` → `true`. `git log -1 --format=%P cc43f3e` → one parent. `git grep -n "gh pr create" goals/hub_release/execute.sh` → CREATE_PR bypasses `pr-offer-gate.py`.

---

## 6. The one thing

A ship PR (`release/v*` → `main`) must be merge-commit-only: GitHub ruleset or API merge-method lock so squash and rebase are not legal for that head. Offer text is not a poke-yoke.

---

## 7. Prevention test

If squash had been illegal for #71, GitHub could not have stored `cc43f3e` as the merge of that PR. The body sentence “tags on that merge commit” would have matched the only available button.

---

## 8. Contributing factors

- CREATE_PR does not call `pr-offer-gate.py` (skill says that command is the only offer path).
- ADR 0049 `main_context` refuses a squash *after* it lands (S15), which is detection, not prevention of the click.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Lock merge method for pull requests whose head is `release/v*` and base is `main` to merge commit only. CREATE_PR / offer-gate must use that constraint, not only body prose. |
| Owner | hub maintainer |
| Path | GitHub ruleset on `main`; `goals/hub_release/execute.sh` `CREATE_PR`; `tools/pr-offer-gate.py` |
| Verification | A specimen ship PR cannot be squashed. `allow_squash` for that ruleset is false. |
| Implementation route | not in this record |

---

## 10. Follow-up

RCA-S15 is the squash object. RCA-S04 is the tag-next sentence.
