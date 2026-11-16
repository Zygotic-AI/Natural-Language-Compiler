# Incremental compile

**Summary**

NLC compiles one bound goal at a time and stops when a check fails.

**Paragraph**

NLC compiles one bound goal at a time and stops when a check fails. Each step is small enough that a defect shows up at compile time, in the unit that just changed. You do not write that unit. The compiler does, and the graph records the goal the unit belongs to so a review can start from the goal and land on the code.

**Graph**

```json
{
  "nodes": [
    {
      "id": "goal",
      "type": "concept",
      "label": "Goal"
    },
    {
      "id": "atomic-action",
      "type": "process-step",
      "label": "Atomic action"
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
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    }
  ],
  "edges": [
    {
      "from": "goal",
      "to": "atomic-action",
      "kind": "comprises"
    },
    {
      "from": "gate",
      "to": "emit",
      "kind": "allows"
    },
    {
      "from": "emit",
      "to": "produced-code",
      "kind": "produces"
    }
  ]
}
```
