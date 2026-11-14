# Compiler upgrade

**Summary**

Upgrade moves a pinned repository along the compiler version chain, then regenerates and checks the code.

**Paragraph**

Upgrade walks an application from one pinned compiler version to the next along the version chain. The lock changes because you ran the upgrade. The codebase is then regenerated and checked under the new compiler, still with NLC writing the code and the graph recording what changed.

**Graph**

```json
{
  "nodes": [
    {
      "id": "version-store",
      "type": "concept",
      "label": "Version store"
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
    },
    {
      "id": "adopter",
      "type": "system",
      "label": "Adopter"
    }
  ],
  "edges": [
    {
      "from": "version-store",
      "to": "hub",
      "kind": "part_of"
    },
    {
      "from": "compiler-lock",
      "to": "adopter",
      "kind": "part_of"
    }
  ]
}
```
