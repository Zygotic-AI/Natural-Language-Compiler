# Precise rewrite

**Summary**

Still ahead: one accepted decision regenerates only the code it touches, and release lists the steps that are still unfinished.

**Paragraph**

Still ahead, once the graph can see the blast radius and calls are already accountable. You change a decision, including a swap from one database to another, and the compiler rewrites the units that decision owns. If a policy is only partly accepted, release lists those dirty steps so the queue is on the record. You do not write the replacement code. The audit is the graph of what that decision regenerated.

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
      "id": "blast-radius",
      "type": "concept",
      "label": "Blast radius"
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
      "id": "dirty-predicate",
      "type": "concept",
      "label": "Dirty predicate"
    },
    {
      "id": "ship",
      "type": "process-step",
      "label": "Ship"
    }
  ],
  "edges": [
    {
      "from": "accepted-decision",
      "to": "blast-radius",
      "kind": "requires"
    },
    {
      "from": "blast-radius",
      "to": "emit",
      "kind": "allows"
    },
    {
      "from": "emit",
      "to": "produced-code",
      "kind": "produces"
    },
    {
      "from": "dirty-predicate",
      "to": "ship",
      "kind": "allows"
    }
  ]
}
```
