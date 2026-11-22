# ADR 0040 — Process preflight and remediation (exit early)

- Status: Accepted
- Date: 2026-09-23
- Revision: 2
- Amended-by: [ADR 0061](0061-release-in-seven-steps.md) (revision 2)
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

[ADR 0013](0013-requirements-preflight.md) requires listing all missing requirements at entry. [ADR 0018](0018-human-cli-interview-on-gap.md) requires plain-language gap reporting for humans. [ADR 0022](history/0022-hub-release-fail-early-1.md) orders cheap gates before expensive work.

Processes still fail when the operator starts on the wrong branch, merges the wrong line, or hits a state the tool could have detected—because remediation was left to memory instead of embedded questions and fixes.

## Decision

1. **Default-closed entry.** Every human orchestrator (for a release, **`./release validate`**) runs a **preflight** that checks all known blocking conditions for the current repo state before irreversible or expensive steps.

2. **Exit early with remediation, not mystery.** On `NOT_MET`, the tool prints:
   - **What’s wrong** (one line),
   - **Why it blocks** (which ADR / gate),
   - **Fix** (exact commands or choices),
   - **Not** “you should have remembered X.”

3. **Ambiguity refuses.** When state is ambiguous (wrong branch, version and branch disagree) the tool refuses and names the fix; it does not guess.

## Consequences

- `./release validate` prints the failing check and the next step ([ADR 0061](0061-release-in-seven-steps.md)).
- Other human entrypoints (`./nlc`, `/interview` gap blocks) already align; new orchestrators copy this pattern.

## Rejected

- Failing with a single opaque exit code and no fix path.
- Assuming the operator already knows which `release/v*` branch is canonical.
