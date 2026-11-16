# Nothing changes except through NLC

**Summary**

Still ahead: every change goes through NLC, and verify catches an edit that skipped that path.

**Paragraph**

Still ahead, after call envelopes and before we take over our own repository. Every change goes through NLC. A hand prompt is caught and routed into a compiler skill or command, and verify still catches an edit that skipped that path. The codebase the compiler manages cannot be updated beside the graph. The automated review then covers the whole tree, because nothing entered it through another door.

**Graph**

```json
{
  "nodes": [
    {
      "id": "hand-prompt-route",
      "type": "process-step",
      "label": "Hand-prompt route"
    },
    {
      "id": "interview",
      "type": "process-step",
      "label": "Interview"
    },
    {
      "id": "planit",
      "type": "process-step",
      "label": "PLANIT"
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
      "from": "hand-prompt-route",
      "to": "interview",
      "kind": "allows"
    },
    {
      "from": "hand-prompt-route",
      "to": "planit",
      "kind": "allows"
    },
    {
      "from": "produced-code",
      "to": "verify",
      "kind": "audited_by"
    }
  ]
}
```
