# Verify path

**Summary**

Verify fails the tree when generated code does not match its stamps and gates.

**Paragraph**

Verify, and the deeper verify, walk the compiled tree and fail when generated code does not match its stamps and gates. The result is pass or fail, with the next step when it fails. This is the automated review of the code NLC wrote. The graph and the receipts are what get checked, so the audit does not depend on a person rereading the diff.

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
      "id": "code-adversarial-audit",
      "type": "process-step",
      "label": "Code adversarial audit"
    }
  ],
  "edges": [
    {
      "from": "produced-code",
      "to": "code-adversarial-audit",
      "kind": "audited_by"
    },
    {
      "from": "produced-code",
      "to": "verify",
      "kind": "audited_by"
    }
  ]
}
```
