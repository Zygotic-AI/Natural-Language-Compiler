# Emit pipeline gates

**Summary**

Code is emitted only when the action is on the plan and its decisions are bound.

**Paragraph**

Code is emitted only when the action is on the plan and the decisions for that action are bound. A missing decision stops the compiler. The gate stays closed until the plan and the decisions line up, which is how NLC keeps changes that never entered the graph out of the codebase an audit will later read.

**Graph**

```json
{
  "nodes": [
    {
      "id": "atomic-action",
      "type": "process-step",
      "label": "Atomic action"
    },
    {
      "id": "constraint-bind",
      "type": "process-step",
      "label": "Constraint bind"
    },
    {
      "id": "reverse-adversarial-audit",
      "type": "process-step",
      "label": "Reverse adversarial audit"
    },
    {
      "id": "emit",
      "type": "process-step",
      "label": "Emit"
    }
  ],
  "edges": [
    {
      "from": "atomic-action",
      "to": "constraint-bind",
      "kind": "precedes"
    },
    {
      "from": "constraint-bind",
      "to": "reverse-adversarial-audit",
      "kind": "precedes"
    },
    {
      "from": "reverse-adversarial-audit",
      "to": "emit",
      "kind": "allows"
    }
  ]
}
```
