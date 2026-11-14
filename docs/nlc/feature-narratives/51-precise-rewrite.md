# Precise rewrite

**Summary**

Still ahead: one accepted decision regenerates only the code it touches, and release lists steps that are still unfinished.

**Paragraph**

Still ahead, once the graph can see the blast radius and calls are already accountable. One accepted decision regenerates only the code it touches. Swapping an architecture, such as one database for another, is that decision plus a recompile. If a policy is only partly accepted, release lists the steps that are still unfinished so the queue is on the record. You change the decision. NLC rewrites the units. The audit is the graph of what that decision regenerated.

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
