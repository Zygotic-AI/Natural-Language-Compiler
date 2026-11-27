# ADR 0036 — What humans write

- Status: Proposed
- Date: 2026-11-27
- Revision: 2
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc
- Decision-point: human-writes-goals-requirements-knowledge
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

[ADR 0027](0027-emit-from-prose.md) adds a deterministic compiler from constrained prose into pipeline JSON. It does **not** define what humans may contribute on the happy path. Revision 1 said exactly two things (goal and policy). The product owner’s rule: humans write **three** things.

## Decision

On the happy path a human writes **exactly three** things:

| Human writes | Compiler infers |
| --- | --- |
| **Goals** — outcomes in natural language | Plans, actions, ADR bindings, reverse audit, emit, gates, tests, tags, noun/verb structure |
| **Requirements** — constraints, standards, “must / must not” | ADRs and rules derived from those requirements |
| **Knowledge domains** — facts the compile must not invent | Bindings of those facts into generate |

No other human **authorship** is permitted. Ratification, release, and certified [RCA](../docs/TERMS.md#rca) remain human **judgment** over derived artifacts (C24), not authorship of them.

If the compiler cannot derive a binding, it **refuses and reports the gap** — it does not ask the human to supply plans, ADR ids, rule ids, thought anchors, manifests, or tags.

Intake **policy documents** (the source you import from) are [ADR 0062](0062-constraint-stack.md). This ADR is what the human writes, not the intake stack.

Machine artifacts (for example `.nlc/interview-packet.json`) are **agent-written records** of those three writings, not a fourth human input type.

## Consequences

- [`docs/nlc/compiler/INTENT-SURFACE.md`](../docs/nlc/compiler/INTENT-SURFACE.md) and [`docs/nlc/compiler/MANIFESTO.md`](../docs/nlc/compiler/MANIFESTO.md) state goals, requirements, and knowledge domains.
- [`/interview`](../docs/TERMS.md#interview) skill gate forbids collecting derived artifacts from the human.
- v1 binder: [`tools/fitness-nlc-0036-inference-only.py`](../tools/fitness-nlc-0036-inference-only.py) + [`rules/nlc-0036.json`](../rules/nlc-0036.json).

## Related

- [ADR 0017](0017-human-command-surface.md), [ADR 0018](0018-human-cli-interview-on-gap.md)
- [ADR 0027](0027-emit-from-prose.md) (prose → JSON; separate concern)

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** interview skill; intent surface. After accept: fitness requires the three writings.
- **Adjectives that must hold:** happy-path surfaces name goals, requirements, and knowledge domains; they do not ask the human to author ADR/rule/plan ids.
- **Non-goals:** intake stack (0062).
- **Tests:** `tools/fitness-nlc-0036-inference-only.py`.
- **Impact:** interview packet still records the three as agent-written extracts.
