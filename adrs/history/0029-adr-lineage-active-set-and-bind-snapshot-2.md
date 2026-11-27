# ADR 0029 — ADR lineage, ACTIVE set, and bind snapshot

Status: Accepted  
Revision: 2  
Date: 2026-09-22  
Corpus: nlc  
Origin: session decision — policy lineage and binding performance

## Context

Policies change. An ADR that says "encryption must be AES-256" this year becomes "AES-512" next year. We do not want ADRs to grow forever by accumulating cancelled predecessors, and we do not want the binding process to read every historical ADR on every plan.

## Decision

Three documents, not two. The binding process reads only the active set.

### 1. `adrs/INDEX.md` — full history

Every ADR ever written. Each entry carries:

- ADR number
- Created date
- Origin: source document, page, line number (for policy-derived ADRs)
- Status: active | superseded | retired
- Successor pointer: the ADR that replaced it, if any
- Lineage id: groups an ADR with its replacements

Nothing is ever deleted from INDEX. It is the audit trail.

### 2. `adrs/CATALOG.md` — one-line summaries

A flat, human-readable list of every ADR — active or not — with a one-line description. Used for navigation and search. Never used for binding. Cheap to scan, never authoritative for enforcement.

### 3. `adrs/ACTIVE.md` — tips of lineages

Only the current ADR per lineage. This is the **only** file the binding process reads. The rule is absolute: if an ADR is not in ACTIVE, it does not apply. No superseded-check logic lives in the binder. Lineage resolution happens once, at retirement time, when ACTIVE is updated.

## Lineage rule

When a decision is rewritten (same law, new wording or a changed choice):

1. Copy the current file byte-for-byte to `adrs/history/NNNN-slug-R.md` (`R` is the previous revision).
2. Edit `adrs/NNNN-slug.md`. Increment `Revision:`. Same number. Same path.
3. INDEX keeps that number. ACTIVE still lists it if it is law.
4. Previous bytes stay in `adrs/history/`. They are not current law.

When a decision is revoked, superseded, rejected, or removed:

1. Put that status in the header.
2. Move the file to `adrs/history/` with the revision suffix. No current file remains in `adrs/`.
3. INDEX keeps the row and the status. ACTIVE drops it.

A new ADR number is a different decision, not a reword. How the copy, move, and independent signatures work is [ADR 0059](0059-adr-revision-and-history.md).

Example: ADR 0051 revision 1 lives in `adrs/history/`. ADR 0051 revision 2 is `adrs/0051-hub-own-produce-principles.md`. One current file, past bytes available.

## Bind snapshot

A plan snapshots the ACTIVE set at bind time. This gives reproducibility: you can prove exactly which rules a given emit was checked against.

A freshness check runs between bind and emit. If ACTIVE changed in that window, the plan fails and must re-bind. This gives freshness: a policy change mid-flight is caught, not silently applied to a stale plan.

Both, not either/or.

## Why three documents, not two

INDEX and CATALOG could be merged, but they serve different jobs with different shapes. INDEX carries lineage edges and origin citations — structured, audit-grade. CATALOG is a flat readable list for humans. Merging them makes both worse. The split is load-bearing, not cosmetic.

## Consequences

- Binder reads only `adrs/ACTIVE.md`. No history traversal at bind time.
- Retiring an ADR is a single, explicit operation: set the header status, move the file to `adrs/history/`, update INDEX, drop it from ACTIVE.
- Policy-to-ADR compilation (page/line extraction) remains a separate process; this ADR defines the storage and binding contract, not the extraction mechanism.
- Tools (lineage resolver, ACTIVE freshness gate, bind snapshot) are gaps — law first, as usual.

## Open questions (implementation, not principle)

- Exact data structure of lineage edges in INDEX
- Soft vs hard retirement semantics
- Cross-lineage conflict detection when two active ADRs from different lineages conflict
