# ADR 0064 — Where lifecycle state lives

- Status: Proposed
- Date: 2026-11-27
- Revision: 1
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc
- Decision-point: lifecycle-state-location
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

Compile-guide work remembered itself in `.nlc/work-queue.json`, `.nlc/pipeline-state.json`, `.nlc/requirements-sync-pending.json`, and `.nlc/last-requirement-change.json` ([ADR 0019](0019-guided-orchestration.md) revision 1). Per-item side files are not where lifecycle state belongs.

## Decision

1. **Header.** Each governed item’s lifecycle state lives in **its own document header**. No per-item state files.
2. **Scope is lifecycle state only.** Pins (`integrity/nlc-version.json`, `.nlc/lock.json`), emit manifests, interview packet, `verified.json`, before-generate stamps, and `.nlc/verbs.json` are not this ADR.
3. **0019 files.** The four work-queue JSON files named above fall under this ADR. Their facts move into document headers (the item’s own file, or `.nlc/compile-guide-session.md` for session resume that is not a per-item fact). Dashboard and `./nlc` **scan headers**. They do not persist `.nlc/work-queue.json`.
4. **This ADR does not say** how fingerprints are compared or how parents are updated. That is [ADR 0065](0065-type-dependency-and-upward-walk.md).
5. **No “no side json files” rule.** Pins, manifests, `verbs.json`, [ADR 0012](0012-rule-adoption-conflicts.md)’s overrides file, and [ADR 0065](0065-type-dependency-and-upward-walk.md)’s type-dependency file are allowed machine files because other ADRs own them.

## Consequences

- [ADR 0019](0019-guided-orchestration.md) points here and no longer authorizes those JSON files.
- [ADR 0059](0059-adr-revision-and-history.md) keeps ADR **words** (Accepted, Proposed, …). The fact that those words sit in the header is this ADR.
- Flows (including release) sit on this ADR and [ADR 0065](0065-type-dependency-and-upward-walk.md). Flows are not ADRs.

## Rejected

- A per-item `state.json` beside each document.
- Folding type-dependency walk rules into this record.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** dashboard, guide state, compile-guide session document. After accept: queue is a scan of headers.
- **Adjectives that must hold:** those four `.nlc/*.json` names are not written as lifecycle SSOT.
- **Non-goals:** type map and upward walk (0065); pin files (0015).
- **Tests:** `tools/fitness-lifecycle-state-headers.py`; `tools/assert-work-queue-json-not-ssot-fails.py`.
- **Impact:** `./nlc` still shows a queue; the queue is computed from headers.
