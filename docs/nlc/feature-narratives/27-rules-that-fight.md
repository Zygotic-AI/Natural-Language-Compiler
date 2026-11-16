# Rules that fight when you accept them

**Summary**

Two accepted rules that directly contradict each other fail at acceptance, before any code is written.

**Paragraph**

If two accepted rules are a direct contradiction on the same thing, NLC fails when you try to accept them. The compiler will not write code that must both hide a card number and export that card number. The conflict is caught before it enters the codebase, so the automated review never has to reconcile two rules that cannot both be true.

**Graph**

```json
{
  "nodes": [
    {
      "id": "accepted-decision",
      "type": "concept",
      "label": "Accepted decision"
    },
    {
      "id": "rule",
      "type": "concept",
      "label": "Rule"
    },
    {
      "id": "gate",
      "type": "concept",
      "label": "Gate"
    },
    {
      "id": "constraint-bind",
      "type": "process-step",
      "label": "Constraint bind"
    }
  ],
  "edges": [
    {
      "from": "accepted-decision",
      "to": "rule",
      "kind": "codifies_as"
    },
    {
      "from": "gate",
      "to": "constraint-bind",
      "kind": "allows"
    },
    {
      "from": "rule",
      "to": "constraint-bind",
      "kind": "requires"
    }
  ]
}
```
