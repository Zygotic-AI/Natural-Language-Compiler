# ADR 0035 — Charter knowledge and enforcement (R20–R25, R32–R33)

- Status: Proposed
- Date: 2026-11-27
- Revision: 2
- Deciders: Human manager
- Class: A (charter shape)
- Corpus: nlc
- Decision-point: charter-r20-r25-r32-r33
- Ratifies: R20, R21, R22, R23, R24, R25, R32, R33

## Context

Knowledge/drift and enforcement locality rules were bare charter + binders. Integrity zero-variance (R26–R31) already trails to [ADR 0001](0001-zero-variance-integrity.md).

## Decision

Adopt charter §5.6–§5.7 (plus R32–R33):

- **R20–R22:** Charter/contracts/code must agree; impact graphs are generated; superseded ADRs stay marked (trail). Corpus **nlc**. R21’s generated graph is what [ADR 0065](0065-type-dependency-and-upward-walk.md) uses for instance links; this ADR does not describe that walk. R22’s trail is [ADR 0059](0059-adr-revision-and-history.md).
- **R23–R25:** Gates fail illegal noun field writes / copied adjectives; noun adjective tests live with the noun.
- **R32–R33:** Taint single-boundary; no non-OO mutation escape hatches.

## Consequences

- Backlog marks these ids ratified by this ADR.
- R26–R31 remain under ADR 0001.
- Binders unchanged.

## Rejected

- Soft-failing enforcement for “temporary” escapes.
