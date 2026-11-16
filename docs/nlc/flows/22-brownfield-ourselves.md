# Brownfield ourselves

**Summary**

Still ahead: we inventory and take over this compiler's own repository as if we had not written it.

**Paragraph**

Still ahead, after import, the trace graph, accounting, envelopes, precise rewrite, running-app enforcement, and NLC-only changes. The flow is inventory, then plan, then apply, and the tool has to do the inventory even though the repository is our own. NLC writes what is missing and puts the result on the graph so review is a query. The repository pin is already in place so a bad experiment can stay on the last good compiler.

**Graph**

```json
{
  "nodes": [
    {
      "id": "brownfield-inventory",
      "type": "process-step",
      "label": "Brownfield inventory"
    },
    {
      "id": "goal",
      "type": "concept",
      "label": "Goal"
    },
    {
      "id": "hub",
      "type": "system",
      "label": "Hub"
    },
    {
      "id": "compiler-lock",
      "type": "artifact",
      "label": "Compiler lock"
    }
  ],
  "edges": [
    {
      "from": "brownfield-inventory",
      "to": "goal",
      "kind": "allows"
    },
    {
      "from": "compiler-lock",
      "to": "hub",
      "kind": "part_of"
    }
  ]
}
```
