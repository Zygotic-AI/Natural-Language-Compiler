# Install doctor

**Summary**

Doctor checks the install and repairs the common breaks so the compiler can keep managing the codebase.

**Paragraph**

Doctor checks that the install is intact and can repair the common breaks. It restores a compiler that can still manage the codebase when a path, a pin, or a local copy has gone wrong. You run it, and the same compiler is back in place to generate and audit the tree.

**Graph**

```json
{
  "nodes": [
    {
      "id": "install-doctor",
      "type": "process-step",
      "label": "Install doctor"
    },
    {
      "id": "install",
      "type": "process-step",
      "label": "Install"
    },
    {
      "id": "version-store",
      "type": "concept",
      "label": "Version store"
    }
  ],
  "edges": [
    {
      "from": "install-doctor",
      "to": "install",
      "kind": "allows"
    },
    {
      "from": "install",
      "to": "version-store",
      "kind": "produces"
    }
  ]
}
```
