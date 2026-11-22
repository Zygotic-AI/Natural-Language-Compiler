# [ADR](../docs/TERMS.md#adr) 0025 — Belief: no blame, climb upstream, buck stops here

- Status: Accepted
- Date: 2026-09-22
- Revision: 2
- Amended-by: [ADR 0061](0061-release-in-seven-steps.md) (revision 2)
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc

## Context

[`docs/nlc/compiler/MANIFESTO.md`](../docs/nlc/compiler/MANIFESTO.md) now states the belief layer. Unbound manifesto text is not a [rule](../docs/TERMS.md#rule). [ADR](../docs/TERMS.md#adr) 0024 is the factory spine. This [ADR](../docs/TERMS.md#adr) reduces the belief to if/then so RCA cannot stop at “the agent” or at a local environment tweak.

No new **R** id (R27). Rules live in [`rules/nlc-0025.json`](../rules/nlc-0025.json).

## Decision

1. A [defect](../docs/TERMS.md#defect) names a process that was not suitable. It does not name an agent or a human as the cause.
2. [RCA](../docs/TERMS.md#rca) climbs: the process that allowed the defect, then the process that produced that process, to the top of the causal chain within our control; it does not stop at this repository. The RCA names the level that failed: principle, policy, standard, rule or codified constraint.
3. The fix is judged against the area's written target (pinned by path and sha256), lands at or above the failed level, and retires what it replaces: it adds no more rules, checks or state holders than it retires, unless the owner signs an exception. A closed RCA that does not, or that never touches (adds, changes or removes) a belief, principle, [ADR](../docs/TERMS.md#adr), [rule](../docs/TERMS.md#rule), or [gate](../docs/TERMS.md#gate), is incomplete.
4. Patching emit without changing the process that produced it is a new [defect](../docs/TERMS.md#defect).

## Consequences

- Manifesto Belief section is the prose home.
- v1 binder: this ADR + `rules/nlc-0025.json` + [`integrity/schemas/rca-packet.schema.json`](../integrity/schemas/rca-packet.schema.json) + [`tools/validate-rca-packet.py`](../tools/validate-rca-packet.py) (`fitness-adr-0025-rca-packet.py`).
- `tools/validate-rca-packet.py` refuses a packet with no `failed_level`, no `domain_definition` (path and sha256), a `fix.level` below `failed_level`, or a `fix` that adds more than it retires without `fix.exception` (an owner-signed `.approval.asc` for that RCA record). `fitness-adr-0025-rca-packet.py` runs it on every `docs/rca/*.packet.json` recorded on or after 2026-11-21 and on the known-bad specimens in `examples/rca-packet-net-additive/`, inside `./release validate`.
- Related: [ADR 0024](0024-nlc-factory-spine.md).

## Rejected

- Blame the last session.
- Treat a local env fix as root.
- Two manifesto files.
