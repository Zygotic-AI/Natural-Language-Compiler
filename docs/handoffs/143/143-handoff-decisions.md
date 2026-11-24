# #143 pass 2 handoff - decisions

Source: Richard Pickett's decisions, 2026-11-24, on the #143 planit pass 1 GCA list. This file is binding input for planit pass 2. Where it differs from the pass 1 recommendations, this file wins.

## GCA 12 - "I recommend instead" items block

- This reverses pass 1's recommendation that these items be non-blocking.
- Every "I recommend instead" item blocks execution until the human accepts, rejects or amends it.
- Each response is recorded (see 143-handoff-agreement.md).

## GCA 13 - #88 (grill-me) stays separate

- #88's grill-me gaps are handled in #145, which runs after #143 and #144.
- Correction to pass 1's wording: the #88 packet bug is not "fixed in #144". #144 is the RCA and fix for the interview packet, and it is in progress, not done.
- Pass 2 does not expand #143 to cover #88 or #145.

## GCA 14 - close #123 when #143 ships

- #143 is the single source of truth for this work. Close #123 as a duplicate when #143 ships.

## GCA 6 - #111 is separate, later

- #111 ("Rules that have to work together") is out of scope for #143. It goes to a later milestone, Packs v0.14.0 or Import v0.15.0. Richard picks which.

## GCA 7 - defer #93

- #93 ("Scope control as data") is deferred past these milestones.
- #143 builds the generic GCA report only. The ADR freshness check stays with #93.
- Pass 2 does not wait on #93.

## GCA 11 - source order, and what "wins" means

- Source order: first the issue or manifest, then the interview packet, then the intake (resolution) table.
- "Wins" means quote priority only: when sources agree, or only one speaks, the report quotes the highest-order source.
- Any disagreement between sources is a Conflict raised to Richard. It is never settled silently by the order.

## #180 (ADR 0012 revision) comes first, so nothing is settled silently

- #180, "ADR 0012 revision: any GCA between constraints blocks all progress until the human resolves it", is in flight and comes first in the milestone.
- Until it lands, #143 must not use ADR 0012's tier and rank resolution to pick a winner on its own. No silent tie-breaking.
- Hold every conflict for Richard. Tier or rank may only propose a winner, and Richard must accept it.
