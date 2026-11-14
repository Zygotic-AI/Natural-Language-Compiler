# One-line install

**Summary**

NLC installs with one command on Linux, macOS, or Windows.

**Paragraph**

NLC installs with one command on Linux, macOS, or Windows. Until the compiler is on the machine, it cannot take over a codebase. After it is installed, a new application or an adopted repository is filled and checked by NLC, and you describe what you want instead of writing the source yourself.

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
