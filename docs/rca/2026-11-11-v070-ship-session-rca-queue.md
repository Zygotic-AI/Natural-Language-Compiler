# RCA queue: v0.7.0 ship session

**Date:** 2026-11-11
**Context:** Natural Language Compiler hub. Ship of git tag `v0.7.0` (merge `2e868b1`, pull request #73).
**Status:** instance records + MET packets for RCA-S01…S19. Preventive TODO rows remain open. No remediation in those records.
**Version class:** patch (work list). No new [requirement](../TERMS.md#requirement).

Live checklist: root [`TODO`](../../TODO) section **RCA — v0.7.0 ship session**. Live gap pointer: [`FINDINGS.md`](../../FINDINGS.md) Housekeeping.

This file is the working packet for those rows. It does not replace an instance record. It does not name a producer session or a human manager as the cause ([ADR 0025](../../adrs/0025-belief-no-blame-climb.md) — defects name an unsuitable process).

---

## Scope (operator words)

> make a list of all the misteps in this session
>
> create a complete todo list for us to use for rca - we're going to run an rca on every one.

**Complete** means every misstep listed after that ship, including consequence rows that share a causal chain. **Every one** means do not collapse S15–S17 into S03, and do not skip S18–S19 because they happened before `./release` started.

`v0.7.0` is already tagged and published. These RCAs are not a tag blocker.

---

## How to run one row

Do not ask for an owner signature to start. Investigating does not need `integrity/checker-digest.sha256.approval.asc`.

For the next open id, in order S01 → S19:

1. Copy **Error condition** and **Evidence** from this packet into a new instance record.
2. Follow [`.agents/skills/planit/references/root-cause-analysis-standard.md`](../../.agents/skills/planit/references/root-cause-analysis-standard.md) §4 (bound → reproduce → climb → one thing → record).
3. Name an **unsuitable process**. Climb until this repository (belief / ADR / rule / gate). A closed RCA that never touches those is incomplete ([ADR 0025](../../adrs/0025-belief-no-blame-climb.md)).
4. Write `docs/rca/YYYY-MM-DD-<slug>.md` with the ten sections in the standard §8.
5. Write `docs/rca/YYYY-MM-DD-<slug>.packet.json` and run:

   ```bash
   python3 tools/validate-rca-packet.py docs/rca/YYYY-MM-DD-<slug>.packet.json
   ```

   Stop only on `RCA_PACKET:MET`.
6. Add **one** new `TODO` row for the preventive action named in the record. Do not implement that fix in the RCA pass unless the operator asks.
7. Mark this id `@done` on `TODO` with the record path. Leave this queue table’s Status column as done in the same change.

**Refuse to close a row** when any of these hold: no instance record, packet not MET, the one thing names a person or a session, prevention test sentence missing, or a later row was folded into this one.

Related instance records (do not treat as done for this queue): [`2026-10-31-release-line-push-without-pr.md`](2026-10-31-release-line-push-without-pr.md), [`2026-11-02-pr-offered-before-fitness-success.md`](2026-11-02-pr-offered-before-fitness-success.md).

---

## Index

| Id | Status | Record | Related (do not merge) |
| -- | ------ | ------ | ---------------------- |
| RCA-S01 | done | [`2026-11-11-s01-start-release-dispatch.md`](2026-11-11-s01-start-release-dispatch.md) | |
| RCA-S02 | done | [`2026-11-11-s02-checklist-instead-of-release.md`](2026-11-11-s02-checklist-instead-of-release.md) | S01 |
| RCA-S03 | done | [`2026-11-11-s03-ship-pr-no-squash-stop.md`](2026-11-11-s03-ship-pr-no-squash-stop.md) | S04, S15, S17 |
| RCA-S04 | done | [`2026-11-11-s04-tag-next-after-squash.md`](2026-11-11-s04-tag-next-after-squash.md) | S03, S07, S15 |
| RCA-S05 | done | [`2026-11-11-s05-one-more-merge-while-conflicting.md`](2026-11-11-s05-one-more-merge-while-conflicting.md) | S08, S17 |
| RCA-S06 | done | [`2026-11-11-s06-await-publication-silence.md`](2026-11-11-s06-await-publication-silence.md) | |
| RCA-S07 | done | [`2026-11-11-s07-ship-pr-before-digest-signature.md`](2026-11-11-s07-ship-pr-before-digest-signature.md) | S04, S16 |
| RCA-S08 | done | [`2026-11-11-s08-pr73-before-contain-main.md`](2026-11-11-s08-pr73-before-contain-main.md) | S05, S17 |
| RCA-S09 | done | [`2026-11-11-s09-prep-before-write-record-stall.md`](2026-11-11-s09-prep-before-write-record-stall.md) | S13 |
| RCA-S10 | done | [`2026-11-11-s10-release-line-push-rejected.md`](2026-11-11-s10-release-line-push-rejected.md) | S09 |
| RCA-S11 | done | [`2026-11-11-s11-stale-local-release-branch.md`](2026-11-11-s11-stale-local-release-branch.md) | |
| RCA-S12 | done | [`2026-11-11-s12-empty-highlights.md`](2026-11-11-s12-empty-highlights.md) | |
| RCA-S13 | done | [`2026-11-11-s13-verify-target-after-align-version.md`](2026-11-11-s13-verify-target-after-align-version.md) | S09 |
| RCA-S14 | done | [`2026-11-11-s14-closeout-verify-twice.md`](2026-11-11-s14-closeout-verify-twice.md) | S18, S19 |
| RCA-S15 | done | [`2026-11-11-s15-squash-not-taggable.md`](2026-11-11-s15-squash-not-taggable.md) | S03, S04 |
| RCA-S16 | done | [`2026-11-11-s16-signature-in-pr72-after-ship.md`](2026-11-11-s16-signature-in-pr72-after-ship.md) | S07 |
| RCA-S17 | done | [`2026-11-11-s17-containment-pr74.md`](2026-11-11-s17-containment-pr74.md) | S03, S05, S08, S15 |
| RCA-S18 | done | [`2026-11-11-s18-install-scope-first-land-fitness.md`](2026-11-11-s18-install-scope-first-land-fitness.md) | S14 |
| RCA-S19 | done | [`2026-11-11-s19-features-current-ship-lag.md`](2026-11-11-s19-features-current-ship-lag.md) | S14 |

---

## Shared facts (all rows)

| Fact | Value |
| ---- | ----- |
| Shipped tag | `v0.7.0` |
| Merge that was tagged | `2e868b1` (pull request #73, two parents: `cc43f3e` `d188058`) |
| Squash on `main` | `cc43f3e` (pull request #71, one parent: `3fa590d`) |
| Start-release workflow | [`.github/workflows/start-release.yml`](../../.github/workflows/start-release.yml) |
| Release skill | [`.agents/skills/release/SKILL.md`](../../.agents/skills/release/SKILL.md) |
| Planner | [`tools/nouns/release_state/release_state.py`](../../tools/nouns/release_state/release_state.py) |
| Containment | [`tools/nouns/nlc_release_context/nlc_release_context.py`](../../tools/nouns/nlc_release_context/nlc_release_context.py) (`BLOCKED_MAIN_CONTEXT_NOT_CONTAINED` when a `main` commit is not a merge) |
| Tag-time signature | [ADR 0057](../../adrs/0057-tag-time-checker-digest.md); [`tools/check-checker-digest-signature.py`](../../tools/check-checker-digest-signature.py) |
| Release-line push rule | GitHub ruleset `25824126`; [`docs/github-ruleset-release.md`](../github-ruleset-release.md); RCA [`2026-10-31-release-line-push-without-pr.md`](2026-10-31-release-line-push-without-pr.md) |
| Production trunk | [ADR 0044](../../adrs/0044-hub-release-production-trunk.md) — do not commit ship batches to `main` |
| Merge clicks | Human-only (release skill). Extra clicks in this session: #71, #72, #74 relative to the v0.6.0 shape (start-release → one prep PR → one merge-commit to `main`) |

Pull requests in this session, in time order:

| PR | Base | Merged | Note |
| -- | ---- | ------ | ---- |
| #69 | `release/v0.7.0` | 2026-11-10T22:27:24Z | Install-scope feature (ADR 0060) |
| #70 | `release/v0.7.0` | 2026-11-10T22:45:32Z | Release prep (notes, version, record) |
| #71 | `main` | 2026-11-10T22:49:59Z | Squash. Not taggable |
| #72 | `release/v0.7.0` | after #71 | Tag-time checker-digest armor |
| #74 | `release/v0.7.0` | after #72 | Contain `main` (ours on digest armor) |
| #73 | `main` | after #74 | Merge commit. Tagged |

---

## RCA-S01 — start-release dispatch 403, then an Actions click

**Error condition.** `gh workflow run start-release` returned HTTP 403 (`Resource not accessible by integration`). The producer then instructed the human manager to open GitHub Actions and run **start-release** with `v0.7.0`. The human manager had not had that click as a standing step; prior ships dispatched as the human GitHub identity.

**Evidence to pull.** Workflow [`.github/workflows/start-release.yml`](../../.github/workflows/start-release.yml) (`workflow_dispatch`). Docs [`docs/adoption/RELEASE.md`](../adoption/RELEASE.md) (“Run it from the Actions tab”). Cloud-agent `GH_TOKEN` scopes. Prior `start-release` workflow-run actors for `v0.6.0`. Release skill: run `./release`; do not dump steps.

**Surfaces.** Release skill, start-release workflow permissions, cloud-agent token vs human identity, `docs/adoption/RELEASE.md` wording that always says Actions tab.

**Stop.** Instance record + packet MET. Preventive action tracked separately.

---

## RCA-S02 — checklist instead of `./release` after authorization

**Error condition.** After the operator authorized the cut, the producer emitted a human checklist (create the line, write notes, merge) instead of invoking `./release` from the repo root. The release skill’s job is to run the orchestrator; `RELEASE:NOT_MET` is the named stop.

**Evidence to pull.** [`.agents/skills/release/SKILL.md`](../../.agents/skills/release/SKILL.md) (“Do not instruct the user to… **do it**”). [ADR 0038](../../adrs/0038-no-memory-in-process.md) (no memory in process). Planner first action on a missing `release/v0.7.0` (likely `CREATE_RELEASE_LINE` / start-release). Session transcript before the first `./release`.

**Surfaces.** Release skill gate table vs chat behavior. Whether `CREATE_RELEASE_LINE` failing 403 is a named human decision or a producer-token gap (see S01).

**Stop.** Instance record + packet MET. May share a climb with S01; still a separate error condition (checklist vs 403).

---

## RCA-S03 — ship PR to `main` offered without a squash hard-stop

**Error condition.** Pull request #71 (`release/v0.7.0` → `main`) was offered as the ship merge. The offer body did not make “Create a merge commit or the tag will refuse” a hard stop. GitHub’s default on that repo squashed. `cc43f3e` has one parent.

**Evidence to pull.** `git log -1 --format='%H %p %s' cc43f3e` → `cc43f3e 3fa590d Release v0.7.0 (#71)`. Containment [`nlc_release_context.py`](../../tools/nouns/nlc_release_context/nlc_release_context.py) (`len(fields) < 3` → “is not a merge commit”). [ADR 0044](../../adrs/0044-hub-release-production-trunk.md) tag-on-merge-commit. v0.6.0 ship PR merge shape. Release skill / `pr-offer-gate.py` text. GitHub repo merge-button settings.

**Surfaces.** Offer text, GitHub merge method, planner `INVALID_MERGED` vs containment, no machine gate that the open ship PR requires merge-commit.

**Stop.** Instance record + packet MET. Do not close by pointing at S15 (the squash is the later error condition).

---

## RCA-S04 — “next step is the tag” after #71

**Error condition.** After #71 merged, the producer told the operator the next step was the tag. Two independent refusals were already true: (1) `cc43f3e` is not a merge commit; (2) `integrity/checker-digest.sha256.approval.asc` still covered **v0.6.0** bytes (`RELEASE_TAG_GATE:NOT_MET`).

**Evidence to pull.** Tag gate [`tools/nlc_release_tag_gate.py`](../../tools/nlc_release_tag_gate.py) + [`tools/check-checker-digest-signature.py`](../../tools/check-checker-digest-signature.py). Digest at #71 vs later `bd50f45` / #72. Planner phase after a squash merge to `main`. Chat “tag next” vs `RELEASE:NOT_MET` facts.

**Surfaces.** Release skill “await merge then tag” path that does not re-read tag-gate facts before promising a tag. Jidoka ([`.agents/instructions/jidoka-ssot-output.md`](../../.agents/instructions/jidoka-ssot-output.md)): do not counsel a step the gates refuse.

**Stop.** Instance record + packet MET.

---

## RCA-S05 — “one more merge” while #73 was conflicting

**Error condition.** The producer counted remaining human merges as one (#73) while #73 was `CONFLICTING` against `main` (digest armor hashes: squash tree vs signed tree). The next required merge was #74 into `release/v0.7.0`, then #73.

**Evidence to pull.** GitHub pull request #73 mergeable state before #74. Conflict paths (`integrity/checker-digest.sha256`, armor). Operator messages “How many times do I need to merge?” and “You want me to merge 74 first, then 73?”. Skill: reply with mergeability, not a guessed count.

**Surfaces.** No `gh pr view --json mergeable,mergeStateStatus` (or equivalent) before a merge-count sentence. Offer/update of #73 while `CONFLICTING`.

**Stop.** Instance record + packet MET.

---

## RCA-S06 — await publication, then silence until poked

**Error condition.** `./release` reached `RELEASE:AWAIT publication`. The GitHub Release `v0.7.0` (asset `nlc-0.7.0.tar.gz`) existed about 2026-11-10T23:50Z. The producer did not resume to print `RELEASE:MET v0.7.0 shipped` until the operator asked “how’s it going?” about 2026-11-11T01:18Z. A CI subscription on branch `v0.7.0` did not wake the session.

**Evidence to pull.** `gh release view v0.7.0`. Release workflow publish job timestamps. `cursor-subscriptions` on `github:ci:branch` `v0.7.0`. Release skill done-signals (`complete`). Whether `./release` is supposed to poll, subscribe, or return.

**Surfaces.** Orchestrator stop vs publication. Subscription kind (tag vs branch). No timer fallback. Skill “do it” vs waiting without a wake.

**Stop.** Instance record + packet MET.

---

## RCA-S07 — ship PR to `main` before tag-time signature

**Error condition.** Planner `ALIGN_VERSION` regenerated `integrity/checker-digest.sha256`. Pull request #71 to `main` was opened while `integrity/checker-digest.sha256.approval.asc` still signed the previous digest. [ADR 0057](../../adrs/0057-tag-time-checker-digest.md) requires the owner clearsign at tag time; the tagged commit must carry that armor.

**Evidence to pull.** Digest file SHA before/after ALIGN_VERSION. Armor at #71 vs #72 (`bd50f45`). Tag gate refuse. Release skill / planner order: signature vs PR-to-main. Signing statement format (`tools/check-checker-digest-signature.py`).

**Surfaces.** No planner action “owner signature current before OPEN_PR_TO_MAIN”. Human-only signature is correct; offering the ship PR first is the defect.

**Stop.** Instance record + packet MET. Do not close by pointing at S16 (late signature is the later error condition).

---

## RCA-S08 — #73 opened before containing `main`

**Error condition.** After the #71 squash, `main` had commits not on `release/v0.7.0` that were not merge commits. The producer opened #73 (`release/v0.7.0` → `main`) before merging `origin/main` into the release line. #73 was `CONFLICTING`. Containment (`BLOCKED_MAIN_CONTEXT_NOT_CONTAINED`) also refused tag until a two-parent merge existed.

**Evidence to pull.** [`nlc_release_context.py`](../../tools/nouns/nlc_release_context/nlc_release_context.py) `rev-list origin/main ^release/v*`. Pull request #73 conflict vs #74 (ours on armor). [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) (`main_context = contained | not_contained | unknown`; a squash on `main` is `not_contained`).

**Surfaces.** Planner OPEN_PR_TO_MAIN without `main_contained`. Offer gate does not check mergeable + containment.

**Stop.** Instance record + packet MET.

---

## RCA-S09 — prep surfaces before `WRITE_RECORD`, then stall

**Error condition.** The producer ran `python3 tools/nlc_release_prep_surfaces.py --write --version 0.7.0 --branch release/v0.7.0` (FINDINGS, DESCRIBE, `integrity/hub-release-record.json`) before planner action `WRITE_RECORD`. The next `./release` selected `WRITE_RECORD` and stopped `BLOCKED_WRITE_RECORD_STALLED` because facts did not change.

**Evidence to pull.** Planner `WRITE_RECORD` stall predicate in [`release_state.py`](../../tools/nouns/release_state/release_state.py) / executor. `nlc_release_prep_surfaces.py`. Git history on `release/v0.7.0` around `62fd3bd`. Order in [`docs/adoption/RELEASE.md`](../adoption/RELEASE.md): prep → record → commit.

**Surfaces.** Release skill closeout vs orchestrator ownership of prep. Stall message that implies “commit by hand” instead of “let WRITE_RECORD own the file”.

**Stop.** Instance record + packet MET.

---

## RCA-S10 — commit on local `release/v0.7.0`, push rejected

**Error condition.** After stall, the producer committed “Release v0.7.0” on local `release/v0.7.0` and `git push origin release/v0.7.0` was rejected by ruleset `25824126` (pull request required; fitness required). Work was replayed on `cursor/v070-release-prep-326d` as pull request #70.

**Evidence to pull.** RCA [`2026-10-31-release-line-push-without-pr.md`](2026-10-31-release-line-push-without-pr.md) (same class: planner `PUSH_FAST_FORWARD` / producer push of `release/*` before that commit is a PR head with green fitness). Planner action that produced the local commit (`COMMIT` then `PUSH_*`). v0.6.0 prep shape (work branch + PR into `release/*`).

**Surfaces.** Known open RCA: planner still chooses direct push. This session repeated that class instead of starting on a non-`release/*` branch.

**Stop.** Instance record + packet MET. May cite 2026-10-31 as prior; this row is the 2026-11-10 recurrence (a new defect if that RCA’s preventive action is still unimplemented).

---

## RCA-S11 — tag-time `./release` on a stale local release branch

**Error condition.** Containment reads the **local** `release/v*` name. Local `release/v0.7.0` was behind `origin/release/v0.7.0`, so `./release` reported `BLOCKED_MAIN_CONTEXT_NOT_CONTAINED` until a fast-forward. The remote line already contained `main`.

**Evidence to pull.** [`nlc_release_context.py`](../../tools/nouns/nlc_release_context/nlc_release_context.py) which ref it diffs. Executor fetch/pull before containment. Resume JSON vs local SHA. Session `git fetch` / `git merge --ff-only` around tag time.

**Surfaces.** Orchestrator does not fetch/ff the desired release line before grading containment. Skill resume probe lists branches but tag path skipped a fetch.

**Stop.** Instance record + packet MET.

---

## RCA-S12 — empty Highlights on first `WRITE_NOTES`

**Error condition.** `./release` action `WRITE_NOTES` wrote `docs/adoption/RELEASE-v0.7.0.md` with an empty `## Highlights` (placeholder). Gate: [`tools/nouns/release_notes/release_notes.py`](../../tools/nouns/release_notes/release_notes.py) `Highlights section is empty`. `RELEASE:NOT_MET`. Highlights are human-only when invalid; the producer filled them after the refuse instead of before the first WRITE_NOTES, or the draft writer left a placeholder the skill already knows is invalid.

**Evidence to pull.** `release_notes.py` empty-Highlights check. Release skill “Human-only: … release notes **Highlights** content when invalid”. First `RELEASE-v0.7.0.md` commit vs later highlights. ADR 0060 / install-scope facts that belonged in Highlights (already known before `./release`).

**Surfaces.** Draft generator emits a known-invalid Highlights. Skill does not write Highlights before invoking WRITE_NOTES when the ship story is already known.

**Stop.** Instance record + packet MET.

---

## RCA-S13 — `VERIFY_TARGET` after `ALIGN_VERSION` with 0.6.0 prep surfaces

**Error condition.** Planner `ALIGN_VERSION` set `integrity/nlc-version.json` to `0.7.0`. The next verify still saw FINDINGS / DESCRIBE / `hub-release-record.json` at `0.6.0`. `VERIFY_TARGET` failed. The producer then ran prep surfaces by hand (see S09).

**Evidence to pull.** Planner order in [`release_state.py`](../../tools/nouns/release_state/release_state.py) (`ALIGN_VERSION` vs `PREP` vs `WRITE_RECORD` vs `VERIFY_TARGET`). F1 fitness [`fitness-findings-shipped-tag-sync.py`](../../tools/fitness-findings-shipped-tag-sync.py). What VERIFY_TARGET actually runs (`./nlc verify` / release-prep).

**Surfaces.** Order allows version bump before prep surfaces match. Hand repair then causes S09 stall.

**Stop.** Instance record + packet MET.

---

## RCA-S14 — closeout verify failed on stale gate-set manifest

**Error condition.** After committing TODO / FEATURES pin-complete edits, `./nlc verify` failed (`assert-gate-set-manifest-placeholder-sidecar-fails.py` / derived unsigned manifest). The producer ran `python3 tools/regen-derived-release-state.py` and `python3 tools/derive-check-inputs.py --write`, then proved again. Release skill: prove **once** on the final HEAD.

**Evidence to pull.** [`.agents/skills/release/SKILL.md`](../../.agents/skills/release/SKILL.md) closeout step 6 (“Prove once”). `tools/regen-derived-release-state.py`. Files that moved the gate-set / content tree (TODO, FEATURES). Landmine name from the failing verify.

**Surfaces.** Closeout does not regen derived state after those files. Skill “prove once” vs prove → remanifest → prove.

**Stop.** Instance record + packet MET.

---

## RCA-S15 — #71 squash is not a taggable merge

**Error condition.** GitHub stored #71 as squash `cc43f3e` (single parent). Containment and tag-on-merge-commit both refuse. This is the observed git object, not the offer text (that is S03).

**Evidence to pull.** `git cat-file -p cc43f3e` parents. `nlc_release_context.py` message `{commit[:12]} is not a merge commit`. Tag was later `2e868b1` (two parents). GitHub merge method for Zygotic-AI/Natural-Language-Compiler.

**Surfaces.** Repo allows squash onto `main` for a `release/v*` ship PR. No ruleset “merge commit only” on that path. Planner tagged neither the squash nor a reset of `main` (correct refuse); extra PRs were the cost.

**Stop.** Instance record + packet MET. Independent of S03 (offer) even if the one thing is related.

---

## RCA-S16 — tag-time signature arrived in #72, after the ship PR

**Error condition.** Owner clearsign of `integrity/checker-digest.sha256` (Content-SHA256 `a1aa43f98e48b657c1ab96dc7dc3021560659c88097fba5220f3f7d9883247bb`, armor committed `bd50f45`) landed via pull request #72 **after** #71. The operator was asked to sign after they had already merged a ship PR.

**Evidence to pull.** Armor file history. ADR 0057. Signing block in chat vs `tools/check-checker-digest-signature.py` expected statement. Order vs v0.6.0 (signature on the line before the ship PR).

**Surfaces.** No “signature current” gate before offering PR-to-main. Human signature round-trip is required; **when** it is requested is the process.

**Stop.** Instance record + packet MET.

---

## RCA-S17 — #74 existed only to contain the squash

**Error condition.** Branch `cursor/v070-contain-main-326d` / pull request #74 merged `origin/main` into `release/v0.7.0` with ours on digest armor so #73 could merge. That PR does not exist in the v0.6.0 ship shape. It existed because of S15 + S08.

**Evidence to pull.** PR #74 commits and conflict resolution. Containment after #74 vs before. Operator merge-count friction.

**Surfaces.** Same as S08/S15 at the next climb, but the error condition is “an extra containment PR was required.” Climb until the process that makes containment-after-squash a normal ship step.

**Stop.** Instance record + packet MET.

---

## RCA-S18 — first land of install-scope failed fitness / CI

**Error condition.** The ADR 0060 (install global vs local pin) slice failed hub fitness / CI on first land: pipeline-blockers stamp, `hub_tool()` missing on `nlc-launch`, untracked landmines not in the gate-set. Reruns followed.

**Evidence to pull.** Pull request #68 / #69 fitness logs. `tools/ci_fitness.py` failures. `hub_tool()` binder `fitness-requirements-hub-entrypoints.py`. Gate-set / untracked landmine checks. Install-scope files (`scripts/install.sh`, launchers, `fitness-install-scope*`).

**Surfaces.** Produce path that can offer a PR before `./nlc verify` MET on that HEAD ([`tools/pr-offer-gate.py`](../../tools/pr-offer-gate.py); RCA [`2026-11-02-pr-offered-before-fitness-success.md`](2026-11-02-pr-offered-before-fitness-success.md)). Local prove-once not applied to the feature slice.

**Stop.** Instance record + packet MET.

---

## RCA-S19 — FEATURES current ship said v0.5.0 while tag was v0.6.0

**Error condition.** `docs/nlc/FEATURES.md` header still said current ship **v0.5.0** after tag **v0.6.0** and `integrity/nlc-version.json` **0.6.0**. F1 / product-features SSOT ([`.agents/instructions/product-features-ssot.md`](../../.agents/instructions/product-features-ssot.md)). Aligned only when marking the pin-a-repo TODO done, during v0.7.0 closeout.

**Evidence to pull.** FEATURES.md history between v0.6.0 tag and the closeout commit. `fitness-findings-shipped-tag-sync.py` (does it read FEATURES?). Release-prep surfaces (FINDINGS/DESCRIBE/record only?). [ADR 0050](../../adrs/0050-hub-content-tree-hash.md) content tree vs FEATURES.

**Surfaces.** Prep/F1 does not grade FEATURES current-ship. Product-features instruction is chat-only unless a fitness binds it.

**Stop.** Instance record + packet MET.

---

## Closeout of this queue (not an RCA)

Every RCA-S01…S19 row has an instance record, a MET packet, and a `TODO` `@done` line with that path. Preventive actions remain open as separate `TODO` rows. No remediations were implemented in this pass.

**No ADR, reason:** these records apply the existing Planit RCA standard and [ADR 0025](../../adrs/0025-belief-no-blame-climb.md) (defects name an unsuitable process). They do not change a published contract or mint a new requirement. Preventive work, if taken, may need ADRs later.
