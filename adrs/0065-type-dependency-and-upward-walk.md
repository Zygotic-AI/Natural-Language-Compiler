# ADR 0065 — How lifecycle state is worked out

- Status: Proposed
- Date: 2026-11-27
- Revision: 1
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc
- Decision-point: lifecycle-state-computation
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

Where state lives is [ADR 0064](0064-lifecycle-state-in-document-header.md). This record is how that header stays true when a child changes. Charter R21 (impact graphs are generated, not a parallel hand JSON of instance links) is already ratified by [ADR 0035](0035-charter-knowledge-and-enforcement.md). R20–R22 stay corpus `nlc`.

## Decision

1. **Type-dependency file.** `integrity/type-dependency.json` holds rules about **types** (which type depends on which type). It is not a list of instances.
2. **Instance links.** Links between actual items are embedded by the process that creates them (`Depends-On:` in the header), or taken from the **generated graph**. That satisfies R21 / charter 5.6 / [ADR 0035](0035-charter-knowledge-and-enforcement.md). This ADR does not restate R21.
3. **Upward walk.** One set of scripts walks **up**, compares fingerprints ([ADR 0050](0050-evidence-identity-content-not-history.md): content, not git ids), and writes header state on the parent ([ADR 0064](0064-lifecycle-state-in-document-header.md)).
4. **Fingerprint in the header.** Writing fingerprints into headers creates extra commits. That cost is accepted.
5. **Flows sit on top.** Release and other flows use this walk. They get no ADR of their own.

## Consequences

- `python3 tools/nlc-state-walk.py` is the walker.
- A child leaving Accepted walks up; the parent header is no longer Accepted; the next release gate names the dependency ([ADR 0061](0061-release-in-seven-steps.md)).

## Rejected

- A second type-dependency file per flow.
- Hand-maintained instance link lists that duplicate the generated graph.
- A “no side json files” slogan in this ADR. The type-dependency file is this ADR’s file.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** `nlc-state-walk`; type-dependency JSON. After accept: release goal and compile-guide resume call the walker.
- **Adjectives that must hold:** instance links are not a hand duplicate of the generated graph; type rules live in one file.
- **Non-goals:** where the header field lives (0064); R21 ratification text (0035).
- **Tests:** `tools/fitness-type-dependency.py`; `tools/assert-state-walk-child-drop-fails.py`.
- **Impact:** parent headers update when child bytes or status change.
