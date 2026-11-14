# Rule receipts in code

**Summary**

Generated code carries markers that say which rule is enforced there.

**Paragraph**

Generated code carries markers that say which rule is enforced there. You can ask where a tag is applied and get a location in the tree NLC wrote. Those receipts are what an audit follows. A code review or a compliance review becomes a lookup from the marker back to the decision, on code the compiler produced.

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
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    },
    {
      "id": "audit",
      "type": "concept",
      "label": "Audit"
    }
  ],
  "edges": [
    {
      "from": "rule",
      "to": "produced-code",
      "kind": "constrains"
    },
    {
      "from": "produced-code",
      "to": "audit",
      "kind": "audited_by"
    }
  ]
}
```
