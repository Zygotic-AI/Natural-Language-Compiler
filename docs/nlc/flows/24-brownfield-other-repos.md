# Brownfield on other repos

**Summary**

Still ahead: the same takeover path runs on repositories we did not write, until that path is right.

**Paragraph**

Still ahead, after the first cut on ourselves. Inventory, plan, and apply run on trees we did not write. NLC takes over the codebase, generates what the decisions require, and records it on the graph so code review and compliance review are queries. One successful pass on our own tree is not yet this claim.

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
      "id": "compiled-system",
      "type": "system",
      "label": "Compiled system"
    },
    {
      "id": "adopter",
      "type": "system",
      "label": "Adopter"
    }
  ],
  "edges": [
    {
      "from": "brownfield-inventory",
      "to": "goal",
      "kind": "allows"
    },
    {
      "from": "compiled-system",
      "to": "adopter",
      "kind": "part_of"
    }
  ]
}
```
