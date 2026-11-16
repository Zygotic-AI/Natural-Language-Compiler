# Knowledge facts before generate

**Summary**

Interview produces a Knowledge fact and a Before-generate stamp, and the Gate allows Emit only from that stamp.

**Paragraph**

Interview produces each Knowledge fact, and those facts produce the Before-generate stamp. The Gate sits between that stamp and Emit. The Gate allows Emit when the Before-generate stamp is the one Interview bound.

**Graph**

```json
{
  "nodes": [
    {
      "id": "interview",
      "type": "process-step",
      "label": "Interview"
    },
    {
      "id": "knowledge-fact",
      "type": "concept",
      "label": "Knowledge fact"
    },
    {
      "id": "before-generate-stamp",
      "type": "artifact",
      "label": "Before-generate stamp"
    },
    {
      "id": "gate",
      "type": "concept",
      "label": "Gate"
    },
    {
      "id": "emit",
      "type": "process-step",
      "label": "Emit"
    }
  ],
  "edges": [
    {
      "from": "interview",
      "to": "knowledge-fact",
      "kind": "produces"
    },
    {
      "from": "knowledge-fact",
      "to": "before-generate-stamp",
      "kind": "produces"
    },
    {
      "from": "before-generate-stamp",
      "to": "gate",
      "kind": "allows"
    },
    {
      "from": "gate",
      "to": "emit",
      "kind": "allows"
    }
  ]
}
```
