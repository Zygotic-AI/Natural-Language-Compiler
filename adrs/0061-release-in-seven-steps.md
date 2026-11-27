# ADR 0061 — Release readiness checklist

- Status: Proposed
- Date: 2026-11-27
- Revision: 3
- Deciders: Human manager
- Class: F (process / hub release)
- Corpus: nlc
- Decision-point: release-readiness-checklist
- Supersedes: [ADR 0022](history/0022-hub-release-fail-early-1.md), [ADR 0045](history/0045-hub-release-identity-1.md), [ADR 0049](history/0049-release-planner-owns-stops-1.md), [ADR 0056](history/0056-per-file-adr-detached-signatures-1.md)
- Amends: [ADR 0015](0015-distribution-lock-and-version-store.md), [ADR 0025](0025-belief-no-blame-climb.md), [ADR 0039](0039-single-command-human-surfaces.md), [ADR 0040](0040-process-preflight-remediation.md), [ADR 0044](0044-hub-release-production-trunk.md), [ADR 0048](0048-executable-shape.md), [ADR 0050](0050-evidence-identity-content-not-history.md), [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md), [ADR 0055](0055-staged-activation-of-gate-machinery.md), [ADR 0057](0057-tag-time-checker-digest.md), [ADR 0059](0059-adr-revision-and-history.md)
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

The owner’s comment on issue #126 (2026-11-21 4:50 PM CST, chat message t2375u) named a release sequence. That sequence is executed by the **release goal**, not by this ADR. This ADR is the readiness checklist the goal checks. The product owner (2026-11-27 3:40 PM CT), verbatim:

> Do we have all the issues for this milestone competed? (this would be in the top of the checklist of the release, btw)

## Decision

The **release goal** (`goals/hub_release/`) runs the steps, its gates, and the release record. This ADR is only the **readiness checklist** that goal checks. It does not list commands.

Any future item that can be tested as an indicator of the repo’s readiness is added **here**, not as a new ADR.

### Checklist (order is the gate order)

1. **Milestone issues.** Do we have all the issues for this milestone competed? (this would be in the top of the checklist of the release, btw) All issues for this milestone completed. The goal’s first gate fails and **names each open milestone issue**. Method: the release goal reads the branch it is run on: `git rev-parse --abbrev-ref HEAD`. In GitHub Actions, where HEAD is detached, it reads `GITHUB_REF_NAME` instead. That name must match exactly `^release/v(\d+)\.(\d+)\.(\d+)$`. The captured vX.Y.Z is the version being released. Any other result (main, a change branch, detached HEAD with no ref name) refuses, saying which branch it saw and that a release runs only on release/vX.Y.Z. Milestone: exactly one GitHub milestone (any state) whose title ends with " - vX.Y.Z". Zero or more than one refuses and names what it found. integrity/nlc-version.json is not used to pick the milestone.
2. **Constraints.** Every source document is completed, every ADR is Accepted with its own signature, and every codified constraint is Accepted. Nothing is still imported but unconfirmed. ([ADR 0062](0062-constraint-stack.md), [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md), [ADR 0059](0059-adr-revision-and-history.md).)
3. **Goals.** Every goal is complete. Each atomic action is implemented, bound to its constraints, and passes its gate.
4. **Manifests and audits.** Every producer run in the release has a final manifest whose audit result is pass.
5. **Open questions.** No gaps, conflicts, ambiguities or requests remain open on anything in the release.
6. **Generated files.** Every derived file has been regenerated and matches its source (graph, indexes, release notes).
7. **Gates.** The full release gate profile passes on the release branch head.
8. **Charter agreement.** Charter, contracts and code agree, per R20 ([ADR 0035](0035-charter-knowledge-and-enforcement.md)).
9. **Version.** Version file, release notes and tag name all match the semver.
10. **Signatures.** Every ADR’s own signature verifies with the product owner’s key, checked against a copy kept outside the repo, plus the one release signature.

The goal always re-checks these. Start reports every unfinished dependency, then stops ([ADR 0040](0040-process-preflight-remediation.md) shape). Mid-flow, if a dependency drops, the next gate fails and names it. Resume skips a gate only when fingerprints still match ([ADR 0064](0064-lifecycle-state-in-document-header.md), [ADR 0065](0065-type-dependency-and-upward-walk.md)).

## Consequences

- From superseded ADR 0022: decision 1 (`main` holds the tagged version) stays a trunk rule in [ADR 0044](0044-hub-release-production-trunk.md); notes with real Highlights stay a validate write inside the goal. Its other decisions are dropped.
- No per-branch CI, no required check, no release ruleset. A broken change is found at validate.
- `release.yml` and `integrity/owner-keys/` stay outside the signed set until issue #135. Until then, a release that changes `integrity/owner-keys/` also needs the gate-set manifest signature of ADR 0052 that `fitness-owner-key-trust` checks; it is the one exception to "one signature per release".
- Crew mandate 5k does not apply to NLC releases: `release.yml` publishes the GitHub Release from the tag, and the one release signature is the owner's approval of the release file.
- Validate rewrites `docs/adoption/RELEASE-vX.Y.Z.md` from the merged PR titles on every run, so hand edits to that file are overwritten, and a merge that is not a PR merge commit (`Merge pull request #N`) is not listed.
- Defects found in a release are handled by ADR 0025: an RCA names the level that failed, judges its fix against the area's written target (this record, for releases), and retires at least what the fix adds unless the owner signs an exception. `tools/validate-rca-packet.py` refuses a packet that does not, inside validate.
- The v0.9.0 tag is verified by the v0.8.0 checker; from v0.9.0 on only this record applies.
- [ADR 0039](0039-single-command-human-surfaces.md), [ADR 0044](0044-hub-release-production-trunk.md), and [ADR 0048](0048-executable-shape.md) **point at the release goal**. They do not copy this checklist or the steps.

## Rejected

- Keeping the seven-step command table as this ADR’s law.
- A second ADR for “future readiness checks.”
- Per-tool signatures ([ADR 0055](0055-staged-activation-of-gate-machinery.md)).

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** `goals/hub_release/`; thin `scripts/nlc-release.sh`. After accept: the goal checks this list in order.
- **Adjectives that must hold:** first gate names each open milestone issue; this file has no command table.
- **Non-goals:** step implementation (the goal); sidecar format (0052).
- **Tests:** `tools/fitness-release-readiness.py`; `tools/assert-open-milestone-issue-fails.py`.
- **Impact:** `./release` stays thin; the skill tells the agent to run the goal.
