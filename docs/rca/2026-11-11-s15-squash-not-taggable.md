# RCA: #71 squash object is not a taggable merge

**Date:** 2026-11-11
**Queue id:** RCA-S15
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Independent of RCA-S03 (the offer text). Do not fold S03 into this record.

---

## 1. Error condition

**Observed.** GitHub stored pull request #71 as squash `cc43f3e1d5235edd1a6f3bde1a76939ed18b0795` (single parent `3fa590d61fc1cf181fe35e5364a18953846bf740`, subject `Release v0.7.0 (#71)`), merged 2026-11-10T22:49:59Z.

**Observed (gates).** [`nlc_release_context.py`](../../tools/nouns/nlc_release_context/nlc_release_context.py): `len(fields) < 3` → `{commit[:12]} is not a merge commit` → `not_contained`. [ADR 0044](../../adrs/0044-hub-release-production-trunk.md) tags a merge commit. Tag was later `2e868b1` (two parents: `cc43f3e` `d188058`).

**Observed (repo).** `allow_squash_merge=true` on Zygotic-AI/Natural-Language-Compiler. No ruleset on `main` restricting `release/v*` heads to merge-commit.

**Not this record.** Offer body lacking a hard-stop (RCA-S03). “Tag next” sentence (RCA-S04). Extra containment PR (RCA-S17).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | `cc43f3e` | One parent; cannot tag |
| 3 | GitHub merge | Squash was a legal button |
| 2 | Repo merge methods | Squash, merge, and rebase all allowed |
| 1 | No ruleset on `main` for head `release/v*` | Method is memory |
| 0 | ADR 0044 / 0049 | Tag-on-merge-commit is policy after the object exists |

**Furthest controllable point:** GitHub can persist a squash of a `release/v*` → `main` pull request. Containment detects that object; it does not prevent storing it.

---

## 3. Impact / scope

The squash could not be tagged. Extra PRs #72–#74. v0.6.0 used two-parent `3e098b2` without a repo lock — luck, not a gate.

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-11-08T21:53:01Z | v0.6.0 merge commit `3e098b2` (two parents) |
| 2026-11-10T22:49:59Z | #71 squash `cc43f3e` (one parent) |
| 2026-11-10T23:39:01Z | #73 merge commit `2e868b1` tagged |

---

## 5. Mechanism on reproduction

**Confirmed.** `git log -1 --format='%H %P %s' cc43f3e` → one parent. `git cat-file -p cc43f3e` parents: one. `gh api ... --jq .allow_squash_merge` → true. Containment message class is “is not a merge commit.”

---

## 6. The one thing

GitHub must not be able to store a squash (or rebase) of a pull request whose head is `release/v*` and whose base is `main`. A ruleset (or equivalent API merge-method lock) with `allowed_merge_methods: ["merge"]` on that path makes the one-parent object impossible.

---

## 7. Prevention test

If squash had been illegal for that head/base, GitHub could not have stored `cc43f3e` as the merge of #71. The error condition (a one-parent ship merge) could not have occurred.

---

## 8. Contributing factors

- S03: offer did not lock the method (process of offering; this record is the stored object).
- Detection in `main_context` is after the click.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | GitHub ruleset on `main` for head `release/v*`: merge commit only (`allowed_merge_methods: ["merge"]`). |
| Owner | hub maintainer |
| Path | GitHub rulesets API; document in `docs/github-ruleset-release.md` or a main-ship ruleset doc |
| Verification | A specimen `release/v*` → `main` PR cannot be squashed. `git log -1 --format=%P` of its merge has two parents. |
| Implementation route | not in this record |

---

## 10. Follow-up

S03 remains the offer-text/process record. This record is the git object.
