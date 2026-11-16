# Adversarial review

**Summary**

A second role attacks the plan before any code is emitted, and a failed attack leaves the codebase unchanged.

**Paragraph**

A second role attacks the plan before any code is emitted. The role that writes the plan is not the role that accepts it. The attack looks for missing decisions, unbound work, and steps that would put the wrong code in the tree. When that review fails, NLC stops, and the codebase is unchanged.

**Graph**

```json
{
  "nodes": [
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
