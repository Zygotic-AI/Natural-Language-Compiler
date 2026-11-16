# Greenfield app scaffold

**Summary**

A new application starts with the NLC entry point, the compiler lock, and a CI check, and no product code yet.

**Paragraph**

A new application starts with the NLC entry point, the compiler lock, and a check that runs in continuous integration. The repository has no product code yet and is already set up for the compiler to fill it. From the first generated file, NLC owns the codebase and every later review runs against what the compiler produced.

**Graph**

```json
{
  "nodes": [
    {
      "id": "adopter",
      "type": "system",
      "label": "Adopter"
    },
    {
      "id": "compiler-lock",
      "type": "artifact",
      "label": "Compiler lock"
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
