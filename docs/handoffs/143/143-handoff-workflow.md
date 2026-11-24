# #143 pass 2 handoff - workflow

Source: Richard Pickett's decisions, 2026-11-24, on the #143 planit pass 1 GCA list ([comment](https://github.com/Zygotic-AI/Natural-Language-Compiler/issues/143#issuecomment-7131850558)). This file is binding input for planit pass 2. Where it differs from the pass 1 plan, this file wins.

## 1. GCA timing (pass 1 GCA 1)

- The GCA report runs after PLANIT step 1 (Interview) and before PLANIT step 2 (Plan).
- It runs again after every amendment, until no open GCA remain.
- Execution (PLANIT step 6) starts only when no GCA are open.

## 2. Plan loop gate

- Planning is a loop, not one pass: plan, GCA, resolve with the human, re-plan, GCA again.
- A gate sits on the loop exit. The loop exits to execution only when a full GCA pass finds zero open GCA.
- An open GCA of any kind (gap, conflict or ambiguity) blocks the exit. Resolving it is the only action allowed (see #180, the ADR 0012 revision, in 143-handoff-decisions.md).

## 3. Planit starts the interview

- Planit owns the start of the interview. The human does not run the interview separately and then hand its output to planit.
- When planit begins on a request, it invokes the interview skill as its own step 1. The interview output (the packet) feeds straight into the GCA pass.

## 4. Amendments are direct goal edits, with git history

- This replaces pass 1's proposal of a separate append-only ledger (`.nlc/request-amendments.json`, with the original kept verbatim and amendments as siblings). Drop that ledger design.
- An amendment is a direct edit to the goal or request text itself, made only after the human agrees.
- Git history is the record. The commit that applies the amendment carries the original text (in the diff), the new text, the GCA item it resolves, and a pointer to the human's agreement (see 143-handoff-agreement.md).
- Known-bad: an edit to goal text with no linked agreement must fail.

## 5. Knowledge-domain loop

- The interview packet lists `knowledge_domains`. Each named domain is looped over: planit checks the request against that domain's constraints and runs GCA for it.
- The loop repeats when an amendment or an answer adds or changes a domain. A newly added domain gets its own GCA pass before execution.
- The loop exits only when every domain has had a GCA pass with zero open GCA.
