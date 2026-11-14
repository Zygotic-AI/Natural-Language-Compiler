# NLC concept graph (ontology seed)

Machine-readable **concept ontology** for multi-level diagrams: one node set, two edge classes (`path` and `summary`), so the same subject (e.g. **Produced code**) can relate coarsely to a Goal/ADR bundle and finely to the adversarial audit that follows emit.

This is **not** the runtime [trace graph](../FEATURES.md) product. It shares edge-type vocabulary with that future instance store.

| File | Role |
|------|------|
| [`nodes.json`](nodes.json) | Subjects (compile spine + constraint chain + BBP core) with `granularity` L0–L11 |
| [`edge-types.json`](edge-types.json) | Predicates, arity, `path` vs `summary` rules |
| [`edges.json`](edges.json) | Seed relationships + `expanded_by` / `expanded_as_path` |

Dictionary SSOT for names: [`docs/TERMS.md`](../../TERMS.md). Product intent for instance hops: [`FEATURES.md`](../FEATURES.md) (Trace graph).

---

## Problem this solves

At one level:

- Goal + ADRs **together produce** Produced code

At a finer level:

- Goal → Atomic action → Constraint bind → Reverse adversarial audit → Emit → Produced code → Code adversarial audit

**Produced code** therefore has inbound summary edges (from Goal / ADR / realization bundle) and inbound path edges (from Emit), plus an outbound path/summary edge to **Code adversarial audit**. That is intentional — not duplicate nodes.

---

## Model

### One graph

- **Nodes:** stable `id`, `label`, `granularity`, `kind`, optional `terms_anchor`
- **Edges:** `class` ∈ {`path`, `summary`}, `predicate`, `source`, `target`

### Edge classes

| Class | Use |
|-------|-----|
| `path` | Composition (`comprises`) or sequence (`precedes` / `allows` / `produces` / `audited_by`) |
| `summary` | Coarse story; must expand or be explicitly `asserted_without_path` |

### Expansion

A `summary` edge may set:

- `expanded_by`: list of fine edge ids that justify the summary
- `expanded_as_path`: ordered node ids for UI drill-down

Views:

1. **Summary only** — filter `class === "summary"`
2. **Path only** — filter `class === "path"` (compile spine)
3. **Both** — summary dashed, path solid (see React Flow seed)

### Hyper-style coarse facts (Goal + ADRs → code)

Binary edges cannot express “the combination produces.” This seed uses a **bundle node**:

- `compile-realization` ← `member_of` ← Goal, ADR, Codified constraint  
- `compile-realization` → `bundle_produces` → Produced code  
- that bundle edge lists `expanded_by` / `expanded_as_path` to the fine spine

Equivalent for query stores: a reified n-ary record `{ rel: realizes, members: [...], target: produced-code }` — same semantics, different serialization.

---

## Compile spine (path)

```text
Goal
  --comprises--> Atomic action
  --precedes--> Constraint bind
  --precedes--> Reverse adversarial audit
  --allows--> Emit
  --produces--> Produced code
  --audited_by--> Code adversarial audit
```

Constraint chain (path):

```text
Policy / standard / etc --extracts_to--> Exact quote --codifies_as--> Codified constraint
ADR --codifies_as--> Rule --precedes--> Codified constraint
Atomic action --binds--> Codified constraint
```

---

## Ontology vs runtime trace

| | Concept graph (this directory) | Runtime trace graph (FEATURES upcoming) |
|--|--------------------------------|----------------------------------------|
| Nodes | TERMS / catalog subjects | Instance records with ids |
| Edges | Allowed types + pedagogical seed | Only hops that were written |
| Summary | May expand to a path; docs may assert | Derived from path or human-accepted — never invented |

Do not treat this seed as proof that a hop existed in a compiled system.

---

## Query examples

- **Coarse “what produced this code?”** — inbound `summary` to `produced-code` (`produces_summary`, `constrains`, `bundle_produces`)
- **Fine “what step emitted this code?”** — inbound `path` `produces` from `emit`
- **Fine “what audited this code?”** — outbound `path` `audited_by` to `code-adversarial-audit`
- **Expand Goal→code** — follow `e-sum-goal-produces-code.expanded_as_path`

---

## React Flow view

**This hub repo is the sole SSOT** for concept-graph data. Do not keep a parallel copy in webs or another repo.

| Artifact | Path |
|----------|------|
| Ontology | this directory (`nodes.json`, `edges.json`, `edge-types.json`) |
| React Flow seed | [`docs/diagrams/nlc-concept-graph-spine.json`](../../diagrams/nlc-concept-graph-spine.json) |
| Notes | [`nlc-concept-graph-spine.md`](../../diagrams/nlc-concept-graph-spine.md) |
| Edge filter CLI | [`docs/diagrams/filter-concept-graph-edges.mjs`](../../diagrams/filter-concept-graph-edges.mjs) |

Toggle views by filtering edges on `data.edgeClass` (`summary` | `path`). Summary edges are dashed; path edges are solid.

```bash
# from Natural-Language-Compiler repo root
node docs/diagrams/filter-concept-graph-edges.mjs path
node docs/diagrams/filter-concept-graph-edges.mjs summary
node docs/diagrams/filter-concept-graph-edges.mjs both
```

Downstream sites may *render* a checkout of these files; they must not become a second SSOT.

---

## Validation rules (for later fitness)

1. Unique node `id`; at most one node per `terms_anchor` when set.
2. Published `summary` edges have `expanded_by` or `expanded_as_path` or `asserted_without_path: true`.
3. Spine `path` edges do not skip FEATURES compile-chain steps when claiming that chain.
4. Instance graphs (future) refuse endpoints without recorded ids.

---

## Scope

**In the ontology:** compile spine, constraint chain, BBP core, realization bundle, and the feature subjects a workflow or relationship diagram needs (facts and stamp, verify and harness, install, fingerprint, lock, version store, doctor, CI verify, pack allow-list, change class, retry check, RCA packet, interior function, language and adapter, brownfield inventory, durable engine, checker digest and signature, artifact manifest, run-level index, model-call record, call envelope, dirty predicate, hand-prompt route, pack publisher, signing key, product UI).

The React Flow file is the compile-spine picture only. It does not draw every node.

**Later:** auto-derived summaries, runtime instance store.
