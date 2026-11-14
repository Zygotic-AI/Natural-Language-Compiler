# No editor hooks

**Summary**

The same compile rules apply in every harness, and verify fails if compiled files appear without stamps and gates.

**Paragraph**

NLC does not attach itself to one editor. The same compile rules apply no matter which agent wrote the files. Verify fails if compiled files showed up without the stamps and gates. The compiler's audit of the tree is the review that counts, on the codebase NLC is responsible for.

**Graph**

```json
{
  "nodes": [
    {
      "id": "harness",
      "type": "system",
      "label": "Harness"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    },
    {
      "id": "verify",
      "type": "process-step",
      "label": "Verify"
    }
  ],
  "edges": [
    {
      "from": "harness",
      "to": "produced-code",
      "kind": "writes"
    },
    {
      "from": "produced-code",
      "to": "verify",
      "kind": "audited_by"
    }
  ]
}
```
