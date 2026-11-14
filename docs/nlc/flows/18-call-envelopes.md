# Call envelopes

**Summary**

Still ahead: every agent call carries a predefined envelope that is audited immediately, and a call that does not conform is abandoned.

**Paragraph**

Still ahead, after Planet accounting and before more compile surface is added. The envelope lists the files created, edited, or deleted and the constraints the call must honor. NLC audits it before the call spends itself across the repository. The files in the tree remain the authority if the envelope disagrees with them. Verify still reviews the code the compiler wrote.

**Graph**

```json
{
  "nodes": [
    {
      "id": "call-envelope",
      "type": "artifact",
      "label": "Call envelope"
    },
    {
      "id": "audit",
      "type": "concept",
      "label": "Audit"
    },
    {
      "id": "emit",
      "type": "process-step",
      "label": "Emit"
    },
    {
      "id": "verify",
      "type": "process-step",
      "label": "Verify"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    }
  ],
  "edges": [
    {
      "from": "call-envelope",
      "to": "audit",
      "kind": "audited_by"
    },
    {
      "from": "call-envelope",
      "to": "emit",
      "kind": "allows"
    },
    {
      "from": "emit",
      "to": "produced-code",
      "kind": "produces"
    },
    {
      "from": "produced-code",
      "to": "verify",
      "kind": "audited_by"
    }
  ]
}
```
