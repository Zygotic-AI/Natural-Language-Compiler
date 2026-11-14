# Decision log

**Summary**

An Accepted decision and an ADR each become a Rule, and that Rule constrains the Produced code.

**Paragraph**

An Accepted decision becomes a Rule, and an ADR becomes that same Rule. The Rule constrains the Produced code. A reader follows the Accepted decision or the ADR to the Rule, then to the Produced code.

**Graph**

```json
{
  "nodes": [
    {
      "id": "adr",
      "type": "concept",
      "label": "ADR"
    },
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
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    }
  ],
  "edges": [
    {
      "from": "adr",
      "to": "rule",
      "kind": "codifies_as"
    },
    {
      "from": "accepted-decision",
      "to": "rule",
      "kind": "codifies_as"
    },
    {
      "from": "rule",
      "to": "produced-code",
      "kind": "constrains"
    }
  ]
}
```
