# Tag-time checker signature

**Summary**

At tag time the owner signs a digest of the checker that will audit the codebase.

**Paragraph**

When a compiler version is tagged, the owner signs a digest of the checker. The signature says the checks that will audit your codebase are the checks approved for that tag. Install verification leans on that signature. The automated review of the code NLC writes is pinned to a checker you can identify.

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
      "id": "checker-digest",
      "type": "artifact",
      "label": "Checker digest"
    },
    {
      "id": "checker-signature",
      "type": "artifact",
      "label": "Checker signature"
    },
    {
      "id": "verify",
      "type": "process-step",
      "label": "Verify"
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
      "from": "checker-signature",
      "to": "verify",
      "kind": "allows"
    }
  ]
}
```
