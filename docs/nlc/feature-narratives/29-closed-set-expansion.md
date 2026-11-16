# Closed-set expansion

**Summary**

A new primitive or tag starts as an accepted decision, and the compiler will not invent one while writing code.

**Paragraph**

A new primitive or a new tag starts as an accepted decision. The compiler will not invent a new kind of building block while it is writing code. The set stays closed until you accept the addition. After that, generated code may use it, and the graph records the decision that opened the set so a review can see why the new piece exists.

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
      "id": "primitive",
      "type": "concept",
      "label": "Primitive"
    },
    {
      "id": "tag",
      "type": "concept",
      "label": "Tag"
    }
  ],
  "edges": [
    {
      "from": "accepted-decision",
      "to": "primitive",
      "kind": "allows"
    },
    {
      "from": "accepted-decision",
      "to": "tag",
      "kind": "allows"
    }
  ]
}
```
