# Produce, audit, and ship as separate roles

**Summary**

The role that produces the code, the role that audits it, and the person who releases it are separated.

**Paragraph**

The role that produces the code, the role that audits it, and the person who releases it are separated. The automated audit can pass and the release is still a separate human mark. NLC reviews the codebase it wrote. A person decides when that reviewed tree is released.

**Graph**

```json
{
  "nodes": [
    {
      "id": "emit",
      "type": "process-step",
      "label": "Emit"
    },
    {
      "id": "audit",
      "type": "concept",
      "label": "Audit"
    },
    {
      "id": "ship",
      "type": "process-step",
      "label": "Ship"
    },
    {
      "id": "produce-audit-ship",
      "type": "concept",
      "label": "Produce \u2260 Audit \u2260 Ship"
    }
  ],
  "edges": [
    {
      "from": "emit",
      "to": "produce-audit-ship",
      "kind": "member_of"
    },
    {
      "from": "audit",
      "to": "produce-audit-ship",
      "kind": "member_of"
    },
    {
      "from": "ship",
      "to": "produce-audit-ship",
      "kind": "member_of"
    }
  ]
}
```
