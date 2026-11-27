# ADR 0044 — Hub release production trunk

- Status: Accepted
- Date: 2026-09-25
- Revision: 2
- Amended-by: [ADR 0061](0061-release-in-seven-steps.md) (revision 2)
- Deciders: Human manager
- Ratified-by: Human manager (hub F process; Planit production-trunk plan)
- Class: F (process)
- Corpus: nlc

## Context

[ADR 0022](history/0022-hub-release-fail-early-1.md) orders release gates and keeps version bumps on `release/v*`. [ADR 0039](0039-single-command-human-surfaces.md) requires one command per step (as amended by [ADR 0061](0061-release-in-seven-steps.md)). [ADR 0040](0040-process-preflight-remediation.md) requires preflight and copy-paste remediation.

Operators still had to remember branch policy: feature work landed on `main`, then release tooling expected a different shape (`release/v*`, merge commit tagging). The human contract should be:

1. Never commit to `main` (only merges).
2. `main` HEAD equals last tagged release.
3. Branch from `main`, work on the release line, sync `main` into that branch when others ship.
4. Run the seven commands of [ADR 0061](0061-release-in-seven-steps.md); each prints success or `RELEASE:REFUSED` with the fix.

## Decision

1. **Production trunk.** `main` is **tagged production only**: `main` HEAD commit must equal the newest reachable `v*.*.*` tag commit (or there is no tag yet). Unreleased work lives on **`release/v*`** (release line), not on `main`.

2. **Release steps.** A release line is cut from `main`, filled one change branch at a time, validated, signed, pushed to `main` and tagged by the commands of [ADR 0061](0061-release-in-seven-steps.md).

## Acceptance criteria

- `./release main` refuses when the release branch tree is not the signed tree.
- `./release tag` refuses when the `origin/main` tree is not the signed tree.

## Consequences

- [`scripts/nlc-release.sh`](../scripts/nlc-release.sh) and [`tools/nouns/nlc_release_tag_gate/`](../tools/nouns/nlc_release_tag_gate/) carry the commands.
- [`.agents/skills/release/SKILL.md`](../.agents/skills/release/SKILL.md): agent closeout on the release line; no ship commits to `main`.

## Rejected

- **Feature integration on `main` between tags** — unreleased commits on `main` break production-trunk preflight.
- **Release branch tree is not the signed tree**: `./release main` prints `RELEASE:REFUSED` and pushes nothing.
