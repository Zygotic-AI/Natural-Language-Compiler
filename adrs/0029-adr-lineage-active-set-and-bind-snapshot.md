# ADR 0029 — INDEX, CATALOG, ACTIVE, and bind reads only ACTIVE

- Status: Proposed
- Date: 2026-11-27
- Revision: 3
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc
- Decision-point: adr-index-catalog-active
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

Policies change. We do not want the binding process to read every historical ADR on every plan. Three files, not two. Copy/move of ADR files is [ADR 0059](0059-adr-revision-and-history.md). Status **words** (Accepted = in force) are [ADR 0059](0059-adr-revision-and-history.md). This ADR is the three files and that bind reads only ACTIVE.

## Decision

Three documents. The binding process reads only the active set.

### 1. `adrs/INDEX.md` — full history

Every ADR ever written. Each entry carries number, created date, origin, status, successor, lineage id. INDEX **displays Accepted** for an in-force current file (not a second vocabulary). Nothing is deleted from INDEX.

### 2. `adrs/CATALOG.md` — one-line summaries

A flat, human-readable list of every ADR — in force or not — with a one-line description. Used for navigation. Never used for binding.

### 3. `adrs/ACTIVE.md` — tips of lineages

Only the current ADR per lineage. This is the **only** file the binding process reads. If an ADR is not in ACTIVE, it does not apply. No superseded-check logic lives in the binder.

## Bind snapshot

A plan snapshots the ACTIVE set at bind time. A freshness check runs between bind and emit. If ACTIVE changed in that window, the plan fails and must re-bind.

## What this does not own

- How a rewrite copies bytes to `adrs/history/` and how a revoke moves the file: [ADR 0059](0059-adr-revision-and-history.md).
- Policy compilation: [ADR 0062](0062-constraint-stack.md).
- Overlap of decision-point names: [ADR 0063](0063-adr-decision-point-register.md).

## Consequences

- Binder reads only `adrs/ACTIVE.md`.
- Tools: lineage resolver, ACTIVE freshness gate, bind snapshot.

## Rejected

- Merging INDEX and CATALOG.
- Copy/move procedure in this record.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** lineage-check, bind-snapshot, freshness. After accept: INDEX displays Accepted for in-force.
- **Adjectives that must hold:** bind reads only ACTIVE; INDEX has every number.
- **Non-goals:** history copy (0059); overlap register (0063).
- **Tests:** `tools/fitness-adr-0029-tools.py`.
- **Impact:** adding 0051 and 0052 to ACTIVE in the same change.
