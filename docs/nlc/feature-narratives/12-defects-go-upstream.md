# Defects go upstream

**Summary**

A wrong emit is fixed in the interview, decision, or rule, and a hand edit to generated code fails verification.

**Paragraph**

When generated code is wrong, the miss is in the interview, the decision, or the rule, and that is what gets fixed. A hand edit to a generated file fails verification. NLC keeps the codebase, so the repair goes back through the compiler and the graph updates with it. The audit trail stays intact because the file was never patched beside the record.

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
      "id": "audit",
      "type": "concept",
      "label": "Audit"
    },
    {
      "id": "rca-packet",
      "type": "artifact",
      "label": "RCA packet"
    },
    {
      "id": "interview",
      "type": "process-step",
      "label": "Interview"
    }
  ],
  "edges": [
    {
      "from": "produced-code",
      "to": "verify",
      "kind": "audited_by"
    },
    {
      "from": "audit",
      "to": "rca-packet",
      "kind": "produces"
    },
    {
      "from": "rca-packet",
      "to": "interview",
      "kind": "allows"
    }
  ]
}
```
