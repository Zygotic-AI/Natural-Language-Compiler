# ADR 0044 — Hub release production trunk

- Status: Proposed
- Date: 2026-11-27
- Revision: 3
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc
- Decision-point: production-trunk
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

Operators still had to remember branch policy: feature work landed on `main`, then release tooling expected a different shape. The human contract should be: never commit to `main` (only merges); `main` HEAD equals last tagged release; unreleased work lives on `release/v*`.

## Decision

1. **Production trunk.** `main` is **tagged production only**: `main` HEAD commit must equal the newest reachable `v*.*.*` tag commit (or there is no tag yet). Unreleased work lives on **`release/v*`** (release line), not on `main`.
2. **Release steps.** Cutting the line, filling it, validating, signing, pushing to `main`, and tagging are the **release goal**. This ADR points at that goal. It does not list the steps.

## Acceptance criteria

- `./release main` refuses when the release branch tree is not the signed tree.
- `./release tag` refuses when the `origin/main` tree is not the signed tree.

## Consequences

- [`scripts/nlc-release.sh`](../scripts/nlc-release.sh) stays a thin entrypoint ([ADR 0048](0048-executable-shape.md)) that calls the release goal.
- [`.agents/skills/release/SKILL.md`](../.agents/skills/release/SKILL.md) points at the same goal.

## Rejected

- **Feature integration on `main` between tags.**
- A second copy of the release step table in this record.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** release goal pointer. After accept: this file has no step table.
- **Adjectives that must hold:** `main` is tagged production; unreleased work is on `release/v*`.
- **Non-goals:** readiness checklist (0061).
- **Tests:** release goal tree guards (existing `nlc_release_tag_gate`).
- **Impact:** trunk rule unchanged; steps live on the goal.
