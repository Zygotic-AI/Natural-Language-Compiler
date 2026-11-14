# Install into a specific repo

**Summary**

A repository can pin its own copy of NLC so a machine-wide upgrade leaves that codebase on the compiler you chose.

**Paragraph**

You can install NLC for the whole user, or pin a copy inside one git repository. The repository pin stays put when the machine-wide install moves. Commands in that repository use the pinned compiler, so that codebase is managed and audited by a compiler you chose for it.

**Graph**

```json
{
  "nodes": [
    {
      "id": "install",
      "type": "process-step",
      "label": "Install"
    },
    {
      "id": "version-store",
      "type": "concept",
      "label": "Version store"
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
      "from": "install",
      "to": "version-store",
      "kind": "produces"
    },
    {
      "from": "compiler-lock",
      "to": "adopter",
      "kind": "part_of"
    }
  ]
}
```
