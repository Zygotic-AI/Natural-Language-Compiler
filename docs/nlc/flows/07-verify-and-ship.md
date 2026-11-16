# Verify and ship

**Summary**

Verify fails the tree when generated code does not match its stamps and gates, and ship is a separate human mark after that check passes.

**Paragraph**

After a goal is generated and gated, verify-deep and then verify walk the compiled tree. Pass means the fingerprints and the policy checks agree with what NLC wrote. Ship-check runs only after that, and it still requires a person to accept the release. A green compile is the automated review of the code. Calling it released stays with the person. The concept graph has verify, gate, and ship as subjects, and this flow is the order they run in.

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
      "id": "gate",
      "type": "concept",
      "label": "Gate"
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
    },
    {
      "id": "ship",
      "type": "process-step",
      "label": "Ship"
    }
  ],
  "edges": [
    {
      "from": "gate",
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
    },
    {
      "from": "verify",
      "to": "ship",
      "kind": "allows"
    }
  ]
}
```
