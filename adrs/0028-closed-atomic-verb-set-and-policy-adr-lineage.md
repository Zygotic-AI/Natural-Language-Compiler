# ADR 0028 — Closed atomic verb set

- Status: Proposed
- Date: 2026-11-27
- Revision: 3
- Deciders: Human manager
- Class: B (emit shape / vocabulary) + F (process / enforcement)
- Decision-point: closed-atomic-verb-set
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

The BBA emit process resolves nouns, assigns verbs, tags data, then evaluates a policy overlay before generation. A small closed set of atomic verbs keeps composition honest; compound verbs become sequences. Adopters need to extend the set at their own repo without forking the hub.

Policy compilation and ADR history copy/move lived in revision 2 of this file. Those are other decisions: [ADR 0062](0062-constraint-stack.md) and [ADR 0059](0059-adr-revision-and-history.md).

## Decision

The hub ships a **baseline atomic verb set** — the minimum every compiled system must understand:

`create`, `read`, `write`, `update`, `delete`, `validate`, `emit`, `bind`.

- Every verb an adopter needs beyond this set is a **compound verb**: a named sequence of atomic verbs, each individually gated, plus an outer gate. No compound verb is a primitive.
- The set is **defined at the adopter repo level** (`.nlc/verbs.json` or equivalent), not inside the hub. The hub provides the baseline; the adopter extends it.
- Extending the set is an explicit, gated act: a new verb requires an ADR (or an accepted rule) citing why no compound of existing verbs suffices. The gate warns: *adding verbs is a footgun — every added verb widens the surface the policy overlay and audit must cover.*
- The baseline itself is versioned with the hub; adopters pin via the lock file ([ADR 0015](0015-distribution-lock-and-version-store.md)).
- Interior primitive **functions** are [ADR 0009](0009-primitive-interior-functions.md), not this list.

**Rationale:** a tiny set forces composition, which is where contracts and gates live.

## Consequences

- `docs/bba/VERB-SET.md` documents the set for adopters.
- TERMS keeps `atomic verb` and `compound verb`.
- Policy → extract → codified if/then is [ADR 0062](0062-constraint-stack.md). `docs/bba/POLICY-ADR-LINEAGE.md` points there.
- Conflicts are [ADR 0012](0012-rule-adoption-conflicts.md).
- The footgun warning is normative: an adopter extending the verb set without an ADR fails the contribution gate.

## Rejected

- **Unlimited verb vocabulary.**
- **Hub-owned verb set with no adopter extension.**
- Policy compilation or ADR copy/move in this record.

## Proposal (G-PROPOSE)

- **Change class:** B and F
- **Nouns / verbs / goals touched:** `verb_set_lineage`. After accept: baseline still these eight names.
- **Adjectives that must hold:** baseline list unchanged; extension without an ADR fails.
- **Non-goals:** constraint stack (0062); history copy (0059).
- **Tests:** `tools/fitness-verb-set-lineage.py`; `tools/assert-verb-set-extension-fails.py`.
- **Impact:** `.nlc/verbs.json` remains the adopter extension file (not 0064 lifecycle state).
