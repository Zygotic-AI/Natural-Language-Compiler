# NLC concept graph — compile spine

React Flow seed: [`nlc-concept-graph-spine.json`](nlc-concept-graph-spine.json).

**SSOT:** this hub only — ontology [`docs/nlc/concept-graph/`](../nlc/concept-graph/). No parallel copy in other repos.

## Edge filter (summary vs path)

| `data.edgeClass` | Stroke | Meaning |
|------------------|--------|---------|
| `path` | Solid | Fine spine / composition |
| `summary` | Dashed (accent) | Coarse Goal/ADR/bundle → code |

**Toggle (hub CLI):**

```bash
node docs/diagrams/filter-concept-graph-edges.mjs path
node docs/diagrams/filter-concept-graph-edges.mjs summary
node docs/diagrams/filter-concept-graph-edges.mjs both
```

Same node **Produced code** participates in both classes (inbound summary from Goal/ADR/bundle; inbound path from Emit; outbound path to Code adversarial audit).
