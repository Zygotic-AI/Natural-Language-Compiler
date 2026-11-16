# Hub charter change

**Summary**

A change to the compiler's own practice is classified, proposed, reviewed, ratified, implemented, confirmed, and recorded, in that order.

**Paragraph**

This loop runs when the work changes the hub itself: the charter, the integrity rules, the agent materials, or the tools. The change is classed by risk first. A proposal is written and attacked before implementation. A person ratifies it. Implementation goes through planit, one artifact at a time. Confirm is the compile check, and record writes the decision. Ship is still later, after a human release mark. The class of the change decides how heavy that ceremony is.

**Graph**

```json
{
  "nodes": [
    {
      "id": "change-class",
      "type": "concept",
      "label": "Change class"
    },
    {
      "id": "planit",
      "type": "process-step",
      "label": "PLANIT"
    },
    {
      "id": "audit",
      "type": "concept",
      "label": "Audit"
    },
    {
      "id": "ship",
      "type": "process-step",
      "label": "Ship"
    }
  ],
  "edges": [
    {
      "from": "change-class",
      "to": "planit",
      "kind": "allows"
    },
    {
      "from": "planit",
      "to": "audit",
      "kind": "allows"
    },
    {
      "from": "audit",
      "to": "ship",
      "kind": "allows"
    }
  ]
}
```
