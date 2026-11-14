# Semantic rule apply

**Summary**

Must and forbid rules are checked against the Python NLC generated for tagged goals.

**Paragraph**

Must and forbid rules are applied to the Python the compiler generates, on goals that carry the right tags. The rule is checked against the code NLC emitted. A review of those goals is that check: the graph says the rule applies, and the compiler confirms the code it wrote obeys it.

**Graph**

```json
{
  "nodes": [
    {
      "id": "rule",
      "type": "concept",
      "label": "Rule"
    },
    {
      "id": "codified-constraint",
      "type": "concept",
      "label": "Codified constraint"
    },
    {
      "id": "atomic-action",
      "type": "process-step",
      "label": "Atomic action"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    }
  ],
  "edges": [
    {
      "from": "rule",
      "to": "codified-constraint",
      "kind": "precedes"
    },
    {
      "from": "atomic-action",
      "to": "codified-constraint",
      "kind": "binds"
    },
    {
      "from": "codified-constraint",
      "to": "produced-code",
      "kind": "constrains"
    }
  ]
}
```
