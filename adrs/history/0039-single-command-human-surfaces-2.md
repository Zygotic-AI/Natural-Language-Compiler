# ADR 0039 — Single-command human surfaces

- Status: Accepted
- Date: 2026-09-23
- Revision: 2
- Amended-by: [ADR 0061](0061-release-in-seven-steps.md) (revision 2)
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

[ADR 0017](0017-human-command-surface.md) requires a jargon-free human menu. [ADR 0022](history/0022-hub-release-fail-early-1.md) orders release gates but today exposes multiple operator entry points (`./release`, `./release prepare`, `./release finish`) that imply the human must know which phase they are in and what was already done.

Async work (PR review, merge, CI) is normal; the human surface must still be **one command** that resumes from durable state—not a checklist of separate verbs for verify, merge, push, tag, and test.

## Decision

1. **One primary command per human process.** A hub release is one command per step of [ADR 0061](0061-release-in-seven-steps.md). The owner's only command is `./release sign`.

2. **State is git.** Release commands read branches, tags and committed files, never chat or operator memory.

3. **Decompose internally.** Version, notes, regeneration and the checks are steps inside `./release validate`, aligned with [ADR 0020](0020-human-vs-agent-commands.md). Releasable gate profiles live only in [`integrity/releasable-gates.json`](../integrity/releasable-gates.json); `./release validate` and `./nlc gate` call the same runner.

## Consequences

- [`docs/adoption/RELEASE.md`](../docs/adoption/RELEASE.md) documents the seven commands.
- Tag push remains the moment GitHub Actions builds release artifacts ([`.github/workflows/release.yml`](../.github/workflows/release.yml)).

## Rejected

- Documenting a multi-command release ritual as the norm (“run prepare, then merge, then finish”).
- Expecting humans to track release phase in a spreadsheet or chat.
