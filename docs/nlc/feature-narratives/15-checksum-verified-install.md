# Checksum-verified install

**Summary**

Install refuses a download whose fingerprint does not match the published compiler.

**Paragraph**

The install stores a tagged copy of the compiler and refuses a download that does not match the published fingerprint. The compiler that writes and audits your codebase is the compiler that was released. A bad download stops before it can generate a single file.

**Graph**

```json
{
  "nodes": [
    {
      "id": "install-fingerprint",
      "type": "artifact",
      "label": "Install fingerprint"
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
      "from": "install-fingerprint",
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
