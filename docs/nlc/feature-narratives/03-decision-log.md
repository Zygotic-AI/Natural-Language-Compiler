# Decision log

**Summary**

Accepted decisions are kept, including the ones they replace, so the graph can show which choice each piece of code obeys.

**Paragraph**

Every accepted decision is kept. When a decision is replaced, the previous one stays on record and the new one becomes the law the compiler follows. The log is how the internal graph remembers which human choice a piece of code is obeying. You can look back at what was accepted without reconstructing the meeting from memory.

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
