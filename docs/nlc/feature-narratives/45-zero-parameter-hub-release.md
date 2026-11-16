# Zero-parameter hub release

**Summary**

Maintainers release the compiler itself with one command and no version-bump flags.

**Paragraph**

Maintainers of the compiler cut a ship of NLC with one release command and no version-bump flags. This is how the compiler itself is released. Your application is a separate codebase: NLC still writes it, the graph still records it, and it ships only after its own automated review and a human release mark.

**Graph**

```json
{
  "nodes": [
    {
      "id": "ship",
      "type": "process-step",
      "label": "Ship"
    },
    {
      "id": "version-store",
      "type": "concept",
      "label": "Version store"
    },
    {
      "id": "checker-digest",
      "type": "artifact",
      "label": "Checker digest"
    },
    {
      "id": "checker-signature",
      "type": "artifact",
      "label": "Checker signature"
    }
  ],
  "edges": [
    {
      "from": "version-store",
      "to": "checker-digest",
      "kind": "comprises"
    },
    {
      "from": "checker-digest",
      "to": "checker-signature",
      "kind": "produces"
    },
    {
      "from": "ship",
      "to": "checker-signature",
      "kind": "requires"
    }
  ]
}
```
