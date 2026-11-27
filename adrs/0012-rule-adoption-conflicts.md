# [ADR](../docs/TERMS.md#adr) 0012 — What happens when two constraints conflict

- Status: Proposed
- Date: 2026-11-27
- Revision: 2
- Deciders: Human manager
- Class: F (process)
- Decision-point: constraint-conflict-halt
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

Adopted if/thens can overlap on the same tagged primitive. Not every overlap is a conflict. Real conflicts appear when two adopted obligations on the **same match** cannot both hold.

Revision 1 auto-won by precedence tier and rank. The product owner’s rule: any gap, conflict, or ambiguity between constraints blocks all progress until the human names a winner. Both constraints are annotated. The loser is marked overridden and stays non-binding. Compile reads those notes.

## Decision

1. **Halt.** When two constraints conflict, work **halts** until the human names a winner. There is no automatic tier win. Tiers in [`integrity/adr-precedence.json`](../integrity/adr-precedence.json) may be shown as a proposed winner. They do not settle the fight.
2. **Tool writes the SSOT.** After the human names the pair and the winner, `python3 tools/nlc-precedence-override.py` writes [`integrity/precedence-overrides.json`](../integrity/precedence-overrides.json). Agents do not hand-edit that file as law.
3. **Notes follow.** The same resolution is noted on the ADR, the extracts, and the codified constraints. Compile **reads the notes**. The winner binds. The loser stays in the tree marked `overridden` (non-binding).
4. **Cross-lineage included.** Two active ADRs from different lineages that conflict halt the same way.
5. **Adopt-time gate.** `python3 tools/check-rule-adoption.py <rules-file>` runs before rules are marked in force. A conflict with no override is `ADOPTION:NOT_MET` and names both ids. Emit-time application is unchanged ([ADR 0007](0007-tags-primitives-reduced-adrs.md)).
6. **What a constraint is** is [ADR 0062](0062-constraint-stack.md). This ADR does not redefine the stack.

## Known-bad

Two adopted rules, same match, `must` vs `forbid`, different `precedence_tier`. Revision 1 would auto-win. This revision must `ADOPTION:NOT_MET` until an override exists. Fixture: `examples/rule-adoption-tier-diff/`.

## Consequences

- [`docs/USE-CASES.md`](../docs/USE-CASES.md) [UC14](../docs/TERMS.md#uc14) stays a true conflict example.
- [`tools/check-rule-adoption.py`](../tools/check-rule-adoption.py) no longer returns a silent winner from tier or rank.

## Rejected

- Automatic tier or rank resolution.
- Prompt negotiation at emit time.
- Deleting the losing constraint.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** `check_rule_adoption`; override writer. After accept: compile reads constraint notes.
- **Adjectives that must hold:** a tier-differing conflict without an override is NOT_MET.
- **Non-goals:** constraint stack (0062); verb set (0028).
- **Tests:** `tools/assert-rule-adoption-conflicts-fails.py`; `tools/assert-rule-adoption-tier-diff-fails.py`.
- **Impact:** every real conflict waits for a named winner.
