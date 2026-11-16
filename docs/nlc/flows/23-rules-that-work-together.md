# Rules that work together

**Summary**

Still ahead: rules that must both be true are shown as a resolution you accept, including rules that come from two packs.

**Paragraph**

Still ahead, after we have brownfielded ourselves and have real cases. These are rules that are both required and are not a straight contradiction. Company encryption and a stricter pack's encryption are the example: NLC shows the overlap and a resolution, such as the stricter rule, and you accept that resolution or edit it and accept your edit. The accepted resolution becomes the decision the compiler writes into the code.

**Graph**

```json
{
  "nodes": [
    {
      "id": "requirement-pack",
      "type": "concept",
      "label": "Requirement pack"
    },
    {
      "id": "rule",
      "type": "concept",
      "label": "Rule"
    },
    {
      "id": "accepted-decision",
      "type": "concept",
      "label": "Accepted decision"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    }
  ],
  "edges": [
    {
      "from": "requirement-pack",
      "to": "rule",
      "kind": "constrains"
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
