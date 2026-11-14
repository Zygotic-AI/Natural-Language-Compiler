# Human ship check

**Summary**

Ship-check is the human confirmation that a release is allowed after the automated audits have passed.

**Paragraph**

Ship-check confirms a release is allowed after the automated audits have passed. A successful compile is not permission to ship. You run the check when you are ready to promote the codebase NLC has already generated and reviewed.

**Graph**

```json
{
  "nodes": [
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    },
    {
      "id": "verify",
      "type": "process-step",
      "label": "Verify"
    },
    {
      "id": "ship",
      "type": "process-step",
      "label": "Ship"
    }
  ],
  "edges": [
    {
      "from": "produced-code",
      "to": "verify",
      "kind": "audited_by"
    },
    {
      "from": "verify",
      "to": "ship",
      "kind": "allows"
    }
  ]
}
```
