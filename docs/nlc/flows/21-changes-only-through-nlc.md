# Changes only through NLC

**Summary**

Still ahead: every change goes through NLC, a hand prompt is routed into a compiler skill or command, and verify catches an edit that skipped that path.

**Paragraph**

Still ahead, after call envelopes and before we take over our own repository. A prompt that did not start inside NLC is caught and sent into a skill or an nlc command. An edit that skipped that route still fails verify, because the files are the authority. The codebase the compiler manages cannot be updated beside the graph. The automated review then covers the whole tree.

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
