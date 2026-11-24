# #143 pass 2 handoff - report format

Source: Richard Pickett's decisions, 2026-11-24, on the #143 planit pass 1 GCA list (GCA 4, 5, 8). This file is binding input for planit pass 2.

## Every GCA uses the five-part blocker shape

- This replaces pass 1's proposal to use the five-part shape only when blocking on a single item.
- Every GCA item, whether gap, conflict or ambiguity, is written in the ADR 0018 five-part shape ("Interview the human when input or state is incomplete"):
  1. Problem: one plain-language sentence saying what blocked progress.
  2. What's missing or wrong: the concrete items.
  3. Ask: the direct question only the human can answer.
  4. Remediation choices: the options, with a default suggestion allowed.
  5. Examples: copy-paste commands or prompts where they shorten the loop.
- The three lists (gaps, conflicts, ambiguities) are kept as the grouping. Each item inside them uses the five parts. State this relation to ADR 0018 explicitly in pass 2's ADR text so the two don't conflict.

## The resolution table is input, not a replacement

- The planit resolution table (Information Completion Contract, `references/information-completion-contract.md` Step 0: Layer A placeholders and Layer B blocking facts, each mapped to a value, Waived or Assumption) is an input the GCA pass reads.
- GCA does not replace or rewrite the table.

## The report shows open items only

- The human-facing report lists only open GCA. Resolved items do not appear in it (their history lives in git, per 143-handoff-workflow.md).
- Each open item in the report carries: a summary, a handle (a stable id the human can answer by), details, options, the ask, and examples.

## Correlated GCAs are grouped

- When several GCA share one cause or one decision, they are grouped under one entry so the human answers once.
- The group lists each member's handle. One answer resolves all members of the group.
- When there are no open GCA, the report says "GCA: none".
