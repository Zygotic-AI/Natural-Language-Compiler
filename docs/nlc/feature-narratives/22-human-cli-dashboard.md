# Human CLI dashboard

**Summary**

Running NLC with no arguments shows the queue and a short command map.

**Paragraph**

Running NLC with no extra arguments shows the queue and a short map of commands. You see what the compiler is waiting on: a decision, a check, a regeneration. The dashboard is the human view of work already tracked on the graph, so you direct the compiler instead of editing the code yourself.

**Graph**

```json
{
  "nodes": [
    {
      "id": "planit",
      "type": "process-step",
      "label": "PLANIT"
    },
    {
      "id": "gate",
      "type": "concept",
      "label": "Gate"
    },
    {
      "id": "verify",
      "type": "process-step",
      "label": "Verify"
    }
  ],
  "edges": [
    {
      "from": "planit",
      "to": "gate",
      "kind": "allows"
    },
    {
      "from": "gate",
      "to": "verify",
      "kind": "allows"
    }
  ]
}
```
