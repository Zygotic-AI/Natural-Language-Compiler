# RCA packet

**Summary**

A non-trivial failure is recorded as a process miss, and the fix goes back into the decision before the compiler regenerates.

**Paragraph**

When something non-trivial fails, the record is a process miss: which decision, rule, or step was wrong. The packet records the process, and the fix goes upstream into the interview or the decision. The compiler regenerates from that corrected record, so the codebase and the audit trail move together.

**Graph**

```json
{
  "nodes": [
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
