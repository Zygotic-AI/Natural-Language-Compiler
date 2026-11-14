# Brownfield ourselves

**Summary**

Still ahead: we inventory and take over this compiler's own repository as if we had not written it.

**Paragraph**

Still ahead, after import, the trace graph, accounting, envelopes, precise rewrite, running-app enforcement, and NLC-only changes. We treat this compiler's own repository as a codebase we did not write: inventory, plan, then apply. The tool has to do the inventory even though the repository is our own. That is how NLC learns to take over a real tree, write what is missing, and put the result on the graph so review is automatic. The repository pin is already in place so a bad experiment can stay on the last good compiler.

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
