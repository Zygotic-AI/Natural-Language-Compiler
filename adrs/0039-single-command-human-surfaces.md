# ADR 0039 — Single-command human surfaces

- Status: Proposed
- Date: 2026-11-27
- Revision: 3
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc
- Decision-point: one-command-per-human-process
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

[ADR 0017](0017-human-command-surface.md) requires a jargon-free human menu. Async work is normal; the human surface must still be **one command** that resumes from durable state.

## Decision

1. **One primary command per human process.** The release command list is the **release goal**. This ADR does not list those commands. It points at that goal.
2. **State is git and document headers** ([ADR 0064](0064-lifecycle-state-in-document-header.md)). Commands do not read chat or operator memory ([ADR 0038](0038-no-memory-in-process.md)).
3. **Decompose internally.** Releasable gate profiles live only in [`integrity/releasable-gates.json`](../integrity/releasable-gates.json); the release goal and `./nlc gate` call the same runner.

## Consequences

- [`docs/adoption/RELEASE.md`](../docs/adoption/RELEASE.md) explains without copying the steps. The steps live in [`.agents/skills/release/SKILL.md`](../.agents/skills/release/SKILL.md), which tells the agent to run the release goal.
- Tag push remains the moment GitHub Actions builds release artifacts ([`.github/workflows/release.yml`](../.github/workflows/release.yml)).

## Rejected

- Documenting a multi-command release ritual as this ADR’s law.
- A second copy of the release step table in this record.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** release goal pointer. After accept: this file has no command table.
- **Adjectives that must hold:** one command per human process; release steps are not duplicated here.
- **Non-goals:** readiness checklist (0061); executable shape (0048).
- **Tests:** `tools/fitness-executable-shape.py` (thin `./release` still classifies).
- **Impact:** operators still run one command per process; the release goal owns the machine.
