# Planit

**Summary**

Planit loads the existing record, plans one bound goal, generates that goal, checks it, and stops when a gate fails.

**Paragraph**

One run authorizes the outcome, takes in what is already decided, and writes a plan of single steps. A second role attacks the plan before anything is emitted. Each step is bound to an accepted decision, generated, and gated before the next step starts. Verify checks the tree, and a later execution audit checks that the gates actually ran. Compile can pass and the release is still a separate human mark. You do not write the code. The compiler does, and the graph records which goal each unit belongs to.

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
      "id": "planit",
      "type": "process-step",
      "label": "PLANIT"
    },
    {
      "id": "goal",
      "type": "concept",
      "label": "Goal"
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
      "id": "verify",
      "type": "process-step",
      "label": "Verify"
    },
    {
      "id": "ship",
      "type": "process-step",
      "label": "Ship"
    }
  ],
  "edges": [
    {
      "from": "interview",
      "to": "planit",
      "kind": "allows"
    },
    {
      "from": "planit",
      "to": "goal",
      "kind": "produces"
    },
    {
      "from": "gate",
      "to": "emit",
      "kind": "allows"
    },
    {
      "from": "planit",
      "to": "verify",
      "kind": "allows"
    },
    {
      "from": "verify",
      "to": "ship",
      "kind": "allows"
    }
  ]
}
```
