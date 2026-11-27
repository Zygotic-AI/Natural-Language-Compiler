# ADR 0062 — What a constraint is

- Status: Proposed
- Date: 2026-11-27
- Revision: 1
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc
- Decision-point: constraint-stack
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

Intake documents (regulations, policies, standards) were being treated as if they bound the compile. Conflict handling ([ADR 0012](0012-rule-adoption-conflicts.md)) and the closed verb set ([ADR 0028](0028-closed-atomic-verb-set-and-policy-adr-lineage.md)) had grown extra sentences about policy compiling to ADRs. That is a different decision.

## Decision

1. **Stack.** Intake document → English extracts (cite, quote, context) → codified if/then constraints. Only **codified** constraints bind.
2. **ADRs sit at extract level.** An ADR is the accepted extract of a decision. It must have one or more codified if/then constraints. The ADR is the why; the if/then is what compile runs ([ADR 0007](0007-tags-primitives-reduced-adrs.md) points here for that stack, and at [ADR 0009](0009-primitive-interior-functions.md) for the primitive list).
3. **Source document completed.** A source document is completed when every extract taken from it, and every ADR those extracts became, is Accepted.
4. **Takes** the old “policy compiles to ADR” sentences out of [ADR 0028](0028-closed-atomic-verb-set-and-policy-adr-lineage.md). Copy and move of ADR files stay [ADR 0059](0059-adr-revision-and-history.md). Conflicts stay [ADR 0012](0012-rule-adoption-conflicts.md).

## Consequences

- [`docs/bba/POLICY-ADR-LINEAGE.md`](../docs/bba/POLICY-ADR-LINEAGE.md) points here.
- [ADR 0061](0061-release-in-seven-steps.md) readiness item “constraints completed” checks this stack.
- Lifecycle of these documents is a header field ([ADR 0064](0064-lifecycle-state-in-document-header.md)); how it is walked is [ADR 0065](0065-type-dependency-and-upward-walk.md).

## Rejected

- Treating the intake document as runtime law.
- Letting an ADR bind with no codified if/then.
- A second ADR that restates this stack.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** constraint stack documents; release goal checks completion. After accept: extract and codified-constraint files carry this header state.
- **Adjectives that must hold:** only codified constraints bind; an ADR without a codified if/then is incomplete.
- **Non-goals:** conflict halt (0012); verb set (0028); where state lives (0064).
- **Tests:** `tools/fitness-constraint-stack.py`; `tools/assert-unsigned-codified-does-not-bind-fails.py`.
- **Impact:** compile and release readiness read this stack, not the intake file.
