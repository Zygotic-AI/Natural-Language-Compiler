# Compile spine

**Summary**

A goal splits into atomic actions, those actions bind to constraints, a reverse check confirms the constraints were included, and emit writes the code that a later audit checks.

**Paragraph**

This is the fine path inside generation. The goal comprises atomic actions. Each action binds to the constraints that apply, and a reverse audit refuses the emit if an applicable constraint was left off. Emit produces the code, and a code audit checks that the constraints landed in it. The same path is what the concept graph draws. A review walks these links instead of rereading the tree. The recorded instance of a whole run, with ids on every hop, is the later trace-graph flow.

**Graph**

```json
{
  "nodes": [
    {
      "id": "goal",
      "type": "concept",
      "label": "Goal"
    },
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
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    },
    {
      "id": "code-adversarial-audit",
      "type": "process-step",
      "label": "Code adversarial audit"
    }
  ],
  "edges": [
    {
      "from": "goal",
      "to": "atomic-action",
      "kind": "comprises"
    },
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
    },
    {
      "from": "emit",
      "to": "produced-code",
      "kind": "produces"
    },
    {
      "from": "produced-code",
      "to": "code-adversarial-audit",
      "kind": "audited_by"
    }
  ]
}
```
