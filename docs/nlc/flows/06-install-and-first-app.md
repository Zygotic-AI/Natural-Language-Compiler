# Install and first app

**Summary**

Install puts a fingerprint-checked compiler on the machine, pins the app to one version, and scaffolds an empty repository the compiler will fill.

**Paragraph**

One command installs NLC on Linux, macOS, or Windows, and a download that misses the published fingerprint is refused. The application repository gets a lock so it stays on the compiler version you chose, including a copy pinned inside that repo. Doctor can repair a broken install. A new app starts with the NLC entry point, the lock, and a check that runs in continuous integration. From the first generated file, the compiler owns the codebase.

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
    },
    {
      "id": "ci-verify-workflow",
      "type": "artifact",
      "label": "CI verify workflow"
    },
    {
      "id": "verify",
      "type": "process-step",
      "label": "Verify"
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
    },
    {
      "from": "compiler-lock",
      "to": "adopter",
      "kind": "part_of"
    },
    {
      "from": "ci-verify-workflow",
      "to": "verify",
      "kind": "allows"
    }
  ]
}
```
