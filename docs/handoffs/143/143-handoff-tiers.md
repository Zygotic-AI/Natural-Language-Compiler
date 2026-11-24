# #143 pass 2 handoff - tiers

Source: Richard Pickett's decisions, 2026-11-24, on the #143 planit pass 1 GCA list (GCA 9). This file is binding input for planit pass 2.

## The tier comes from the files touched, not the agent's label

- Today the AWL section 5 tiers (T0 typo or one-line fix, T1 single-file vault edit, T2 new standard, skill, intent or pack, T3 cross-cutting) are named by the agent itself. That stops.
- The tier is derived from the paths the change touches.
- Any change that touches an ADR, a skill, a schema or a gate is automatically tier 2 or higher.

## Known-bad, must be refused

- A change that edits a skill file but is labeled T1 must be refused.

## What each tier gets

- T0 and T1: inline GCA (short, in the flow).
- T2 and higher: the full GCA report (143-handoff-format.md).
