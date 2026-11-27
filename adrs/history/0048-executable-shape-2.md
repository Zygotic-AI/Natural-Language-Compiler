# ADR 0048 — Executable shape

- Status: Accepted
- Date: 2026-10-08
- Revision: 2
- Amended-by: [ADR 0061](0061-release-in-seven-steps.md) (revision 2)
- Redrafted: 2026-11-07
- Deciders: Human manager
- Ratified-by: Human manager (executable shape, 2026-11-07)
- Class: C (goal shape) with class F enforcement
- Corpus: nlc
- Related: [ADR 0061](0061-release-in-seven-steps.md)
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

Wrapper scripts were owning policy, and an unclassified executable did not fail compile.

Boundary-Based Programming is the noun, verb, adjective, and goal practice. Boundary-Based Architecture is the boundary and contract shape. They are not a program that executes the code.

## Decision

1. **Scan set.** Python, shell, workflows, tests, fixtures, generated code, templates, migrations, vendored code, and configuration.

2. **One shape each.** Each scanned file is exactly one of: noun implementation, goal, primitive adapter, thin entrypoint, or contained fixture.

3. **Failure specimens** are contained fixtures. They are not required to conform.

4. **A thin entrypoint** may parse input, call one noun verb or goal, and report the result. It may not own policy or a state machine.

5. **Worked example of 4.** `scripts/nlc-release.sh` is the thin entrypoint for [ADR 0061](0061-release-in-seven-steps.md); the step code lives in `tools/nouns/nlc_release_tag_gate/`.

6. **Kernel.** `tools/nouns/executable_shape/` checks the tree. An exemption list that names its own files fails.

7. **Compile fails** when the unclassified count is not zero. The gate is on only because every scanned file already has a class.

## Consequences

- Install, release smoke, session preflight, and fitness check 1 policy live under `goals/`.
- Version class for this policy is minor.

## Rejected

- A program that executes Boundary-Based Programming.
- An exemption list the kernel can use on itself.
- Turning the gate on while unclassified files remain.
- Folding [ADR 0049](history/0049-release-planner-owns-stops-1.md) into this record. File shape is every scanned file. Planner-owned stops are one goal.

## Proposal (G-PROPOSE)

- **Change class:** C and F
- **Nouns / verbs / goals touched:** `executable_shape`; `scripts/nlc-release.sh` and `nlc_release_tag_gate` as the worked example (ADR 0061). After accept: no new nouns; existing classifier stays the gate.
- **Adjectives that must hold:** unclassified count is zero; a thin entrypoint owns no policy.
- **Non-goals:** planner-owned `./release` stops (ADR 0049); editing ADR 0045 in place; treating Boundary-Based Programming as a running program.
- **Tests:** `tools/fitness-executable-shape.py`; `tools/assert-executable-kernel-exempt-fails.py`.
- **Impact:** every new executable must be one of the five shapes; `scripts/nlc-release.sh` stays a starter.
