# ADR 0063 — One named decision point per ADR

- Status: Proposed
- Date: 2026-11-27
- Revision: 1
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc
- Decision-point: adr-decision-point-register
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

More than one ADR was restating the same decision. The product owner’s rule: every ADR has one and only one scope. A second ADR claiming or restating the same decision point is a defect.

## Decision

1. **One name.** Each ADR declares one `Decision-point:` in its header. That name is the decision it owns.
2. **Register.** `integrity/adr-decision-points.json` lists every current ADR number and its decision-point name. The file is rewritten from headers; it is not hand-kept law.
3. **Overlap fails.** Two current ADRs with the same decision-point name fail the overlap check. A current ADR that restates another current ADR’s decision in its Decision section, instead of pointing, fails the same check when the names collide.
4. **New number means new decision** ([ADR 0059](0059-adr-revision-and-history.md) decision 8). Rewording the same decision keeps the number and copies history.

## Consequences

- Every ADR in this change names a `Decision-point:`.
- `tools/fitness-adr-decision-point-register.py` rewrites the register and refuses duplicates.
- Other ADRs **point** here; they do not copy the overlap rule.

## Rejected

- Two current files for one decision.
- A chat rule that “no two ADRs overlap” with no named register.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** ADR headers; overlap fitness. After accept: every new ADR adds one register row.
- **Adjectives that must hold:** decision-point names in current `adrs/NNNN-*.md` are unique.
- **Non-goals:** constraint stack (0062); ADR history copy/move (0059).
- **Tests:** `tools/fitness-adr-decision-point-register.py`; `tools/assert-adr-decision-point-overlap-fails.py`.
- **Impact:** a second ADR for an owned name cannot land.
