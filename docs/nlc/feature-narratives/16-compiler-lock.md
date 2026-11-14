# Compiler lock

**Summary**

Each application repository is pinned to one compiler version until you choose to move it.

**Paragraph**

Each application repository is pinned to one version of NLC. Moving that pin is a choice for that repository. The lock keeps the graph, the checks, and the generated code on the same compiler, so an audit of the codebase is an audit against a known compiler and not a moving one.

**Graph**

```json
{
  "nodes": [
    {
      "id": "compiler-lock",
      "type": "artifact",
      "label": "Compiler lock"
    },
    {
      "id": "adopter",
      "type": "system",
      "label": "Adopter"
    },
    {
      "id": "version-store",
      "type": "concept",
      "label": "Version store"
    },
    {
      "id": "hub",
      "type": "system",
      "label": "Hub"
    }
  ],
  "edges": [
    {
      "from": "compiler-lock",
      "to": "adopter",
      "kind": "part_of"
    },
    {
      "from": "version-store",
      "to": "hub",
      "kind": "part_of"
    }
  ]
}
```
