# Policy → ADR lineage

Policies are not runtime input. They are **compiled into ADRs**, and ADRs form **immutable lineages**.

## The chain

```text
policy document (regulation, standard, internal rule)
  → extraction prompt (page + line citations)
  → ADR per decision (cites source location)
  → rule set (if/then over tagged datum × atomic verb)
  → overlay evaluation at emit time
```

1. **Extract.** A prompt reads the policy text and proposes candidate decisions, each anchored to exact page and line numbers.
2. **Decide.** Each candidate becomes an ADR. The ADR records the source citation, the decision, and the if/then rules it produces.
3. **Rule.** The ADR's rules enter the overlay: conditions over (datum tag, atomic verb) → obligations.
4. **Change.** When the policy changes, the current ADR is rewritten after a byte-for-byte copy of the previous file is stored under `adrs/history/`. Same number. Same path. [ADR 0059](../../adrs/0059-adr-revision-and-history.md).

## Lineage

A lineage is a chain of immutable ADRs about one decision topic:

```text
adrs/history/0051-…-1.md  →  adrs/0051-….md (revision 2, current tip)
```

- **Active set** = the tip of every lineage. Gates, overlay, audit, and RCA consult only tips.
- **Full history** = every previous revision under `adrs/history/`, plus git. The ADR index surfaces tips.
- **Retired** = a lineage whose policy was withdrawn. Tip marked retired; chain kept for audit; no gate consults it.

## What this solves

- "This year AES-256, next year 512" produces **one active ADR**, not two.
- Audit can still answer "what was required in 2024?" by walking the lineage.
- RCA climbs to the tip that failed, then to the policy change that produced it — no blame, no deleted history.

## What this rejects

- **Silent in-place edits** of accepted ADRs (no history copy).
- **Superseded-but-active** ADRs lingering in the index "for reference."
- **The policy document as runtime input** — the document is the source; the lineage is the law.

## Open

- Lineage data structure (file-per-link vs. index with parent pointers).
- Retirement semantics and retention windows.
- Cross-lineage conflict resolution (covered in principle by ADR 0012; mechanics deferred).

## Hub documents (ADR 0029)

- Binder input: [`adrs/ACTIVE.md`](../../adrs/ACTIVE.md)
- Human catalog: [`adrs/CATALOG.md`](../../adrs/CATALOG.md)
- Full history: [`adrs/INDEX.md`](../../adrs/INDEX.md)
