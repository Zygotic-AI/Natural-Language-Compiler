# RCA: hub prove METs a dirty tree GitHub will not grade

**Date:** 2026-11-20
**Queue id:** RCA-VERIFY-PROCESS-DIRTY-TREE
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (user words):** why this sort of mistake keeps happening — from the perspective I think the entire release verification process is too complicated, not correctly documented, and defective.

Do not fold RCA-S14’s skill-checklist one thing into this record. Do not fold RCA-ADR-0018 (adopter fail text). Do not implement the preventive here.

---

## 1. Error condition

**Observed (GitHub).** On pull request #120, commit `c321b42` (“Record ADR 0018 verify-fail RCA and tell current-ship the tag exists.”), workflow `fitness` job `fitness` (runs `python3 tools/nlc.py --project . verify`) failed. Job `136624040155`, run `44833497792`, 2026-11-20T23:03:47Z.

```text
VIOLATION hub-content-tree-hash b938ecd5308c023b574bf00f20c34615ea1aac2fc8ee835055712841c12d6df2 != content digest c17252f2312eb21d26189b9600caff5589e3b482661fffc157e9d3dcad43e36e
RESULT:NOT_MET
CI:FAIL releasable verify profile
--- stage findings-last-pass-fresh FAIL ---
CI:FAIL full-nlc-audit quick
CI:FAIL fitness-product-completion-p8-closeout
NLC:NOT_MET
```

**Observed (local, same class).** The producer had already reported `python3 tools/ci_fitness.py` → `CI:MET` on the worktree, then `git add` of new RCA files, then push of `c321b42`. Follow-up `b8d1a1c` resynced `integrity/hub-content-tree-hash.txt` after those files were tracked. GitHub on `b8d1a1c` went green.

**Observed (mechanism, this worktree, 2026-11-20).** `content_digest_excluding` hashes `git ls-files` only. `fitness-findings-last-pass-fresh.py` was `RESULT:MET` while `git status --porcelain` showed `?? .nlc/planit-in-progress.json`. An untracked probe file `docs/rca/_rca-untracked-probe.txt` left the digest unchanged (`ok=True`). `git add` of that probe changed the digest (`ok=False`, expected `5ddb68d6…`). Probe removed; no leftover.

**Not this record.** Adopter packet-vs-compile stage rule. Adopter ADR 0018 fail shape. S14’s “insert regen in release-skill Step 1A.”

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | GitHub `fitness.yml` | `./nlc verify` on a clean checkout of `c321b42` → hash `b938ecd5…` ≠ digest `c17252f2…` |
| 4 | Hub prove | Planit step 7 / `python3 tools/ci_fitness.py` MET on the dirty worktree. GitHub runs the same suite via `tools/nlc.py --project . verify` (hub path wraps `ci_fitness.py`). Same checkers; different git object. |
| 3 | Content stamp | `sync_content_tree_hash` / `content_digest_excluding` use `git ls-files`. Untracked paths are invisible. `integrity/hub-content-tree-hash.txt` is itself excluded, so a dirty stamp file can still MET. |
| 2 | Docs and skills | [`docs/nlc/APP-VERIFY.md`](../nlc/APP-VERIFY.md) is adopter-centric. [`docs/nlc/VERIFY-AND-SHIP.md`](../nlc/VERIFY-AND-SHIP.md) says hub `./nlc verify` runs `ci_fitness.py` and stops. Planit prove names `ci_fitness.py` and does not say commit, stamp, or porcelain. Release skill Step 1A is a seven-step closeout (stamp, then prove once, then clean tree) that Planit feature produce does not run. |
| 1 | Prior RCA | [`docs/rca/2026-11-11-s14-closeout-verify-twice.md`](2026-11-11-s14-closeout-verify-twice.md) already named regen-before-prove. **RCA-S14 preventive** is still ☐. That one thing was more skill text. This class kept happening. |
| 0 | Process shape | Prove-then-commit (Planit) vs commit-then-prove (CI). Derived stamps, gate-set remanifest, install hashes, and a second hash model (`worktree_tree_hash` includes untracked) sit beside the `ls-files` digest. Nineteen open RCA preventives add more steps. |

**Furthest controllable point:** hub verify is allowed to MET on a tree GitHub will not check. The process that produces that MET is too many undocumented regen steps around a defective object, not a missing paragraph in the release skill.

---

## 3. Impact / scope

Every hub produce that writes new paths, syncs the content-tree stamp, proves, then `git add`s, can local-MET and CI-red. Recurrence: S14 (stale unsigned manifest / stamp after TODO/FEATURES), S18 (first-land `hub-content-tree-fresh` / unsigned manifest), this branch (`c321b42` → `b8d1a1c`). Extra follow-up commits. Operator cannot trust “verify passed” as “CI will pass.”

---

## 4. Timeline

| Event | Note |
| --- | --- |
| 2026-10-10 | ADR 0050: evidence identity is content, not history. Freshness = recorded content hash equals current content hash. |
| 2026-11-11 | RCA-S14: closeout proved twice after stale derived stamps. One thing: regen in release-skill Step 1A, then prove once. Preventive still open. |
| 2026-11-11 | RCA-S18: first land failed `hub-content-tree-fresh` / unsigned manifest. Same derived-stamp class on a feature slice. |
| This branch, before `c321b42` | New RCA files untracked. Stamp computed. `ci_fitness.py` MET. |
| `c321b42` | Files committed. Stamp still `b938ecd5…` (digest of the pre-add `ls-files` set). |
| GitHub on `c321b42` | Digest of the committed tree is `c17252f2…`. Fitness FAIL. |
| `b8d1a1c` | Stamp resynced after tracked. GitHub green. |
| 2026-11-20 this RCA | Probe: untracked file → last-pass-fresh MET; `git add` → NOT_MET. Porcelain currently `?? .nlc/planit-in-progress.json` and last-pass-fresh still MET. |

---

## 5. Mechanism on reproduction

**Confirmed.** `tools/nouns/evidence_ref/sync_content_tree_hash.py` `content_digest_excluding` runs `git ls-files` and hashes those path bytes. Untracked files do not enter the digest. `fitness-findings-last-pass-fresh.py` compares the recorded stamp to that digest and can MET on a dirty tree. GitHub `actions/checkout` has no untracked producer files, so the digest on CI is the committed set. Stamping before `git add` writes a MET stamp for a different set than the commit. Planit prove does not require porcelain empty. Release skill Step 1A.7 requires porcelain empty *after* prove, which is too late to stop a dirty-tree MET.

A second hash helper already exists: `worktree_tree_hash` in `tools/nouns/evidence_ref/evidence_ref.py` hashes tracked **and** untracked worktree content. The prove stamp does not use it. Two models is part of the complexity, not the one thing.

---

## 6. The one thing

Hub `./nlc verify` (GitHub `fitness.yml`; wraps `tools/ci_fitness.py`) must refuse MET unless `git status --porcelain` is empty, so prove grades the committed tree CI grades.

That is one gate. It replaces the undocumented regen / hash-after-add / prove-then-commit ritual. It is not another skill paragraph (S14 already tried that).

---

## 7. Prevention test

If that refuse had been in place before this session proved, `python3 tools/ci_fitness.py` could not have printed `CI:MET` while the new RCA files were untracked. The producer could not have stamped `integrity/hub-content-tree-hash.txt` against an `ls-files` set that omitted those files, committed `c321b42` with hash `b938ecd5…`, and had GitHub report `b938ecd5… != c17252f2…`. Local prove would have been NOT_MET until the files were committed and the stamp resynced against that HEAD.

---

## 8. Contributing factors

- The entire hub verify/ship path is a pile of commands and checklists: Planit prove (`ci_fitness.py`), GitHub (`./nlc verify` wrapping the same suite), `./nlc verify-deep`, `./nlc ship-check` / `release-audit.py`, `regen-derived-release-state.py`, gate-set remanifest, content-tree stamp, install hashes, Planit identity. APP-VERIFY and VERIFY-AND-SHIP do not describe that pile as one object.
- RCA-S14 preventive still ☐. Skill “regen then prove once” is a recipe. Recipes are not gates. Planit feature produce does not run release Step 1A.
- Including untracked paths in the content digest *without* a clean-tree refuse would make CI worse: local stamp would include files GitHub never checks out.
- `.nlc/planit-in-progress.json` is untracked session state. A porcelain refuse needs that path gitignored (or excluded) so a live Planit session can prove a clean HEAD. Follow-up, not a second root.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Hub fitness (`ci_fitness.py` / `./nlc verify`) NOT_MET when `git status --porcelain` is non-empty. Landmine: dirty or untracked digest-eligible tree cannot MET last-pass-fresh / verify. |
| Owner | hub maintainer |
| Path | `tools/nouns/fitness_findings_last_pass_fresh/fitness_findings_last_pass_fresh.py` (or a sibling fitness both `ci_fitness.py` and hub `./nlc verify` always run). Gitignore or exclude `.nlc/planit-in-progress.json` so session state is not porcelain. |
| Verification | Reproduction in §1: untracked probe + `fitness-findings-last-pass-fresh.py` → `RESULT:NOT_MET` (today it is `RESULT:MET`). Clean HEAD still `RESULT:MET`. GitHub checkout remains MET. |
| Implementation route | not in this record |

---

## 10. Follow-up

Do not add another regen paragraph to `.agents/skills/release/SKILL.md` as prevention of this class. S14 already named that; it did not stop this miss. Detection-only: keep GitHub as the backstop, but that is how the defect is noticed today, not how it is prevented.
