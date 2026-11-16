# Low-code UI

**Summary**

Still ahead, last: a product interface sits on the same compile path, and NLC still writes and reviews the code.

**Paragraph**

Still ahead, last. You describe the application and accept the decisions in a product interface. The flow underneath is the same one: interview, planit, the compile spine, verify, and the graph. The interface waits until that path is the one we are actually shipping, so the screen is built on the real checks.

**Graph**

```json
{
  "nodes": [
    {
      "id": "product-ui",
      "type": "system",
      "label": "Product UI"
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
      "id": "verify",
      "type": "process-step",
      "label": "Verify"
    }
  ],
  "edges": [
    {
      "from": "product-ui",
      "to": "interview",
      "kind": "allows"
    },
    {
      "from": "interview",
      "to": "planit",
      "kind": "allows"
    },
    {
      "from": "planit",
      "to": "verify",
      "kind": "allows"
    }
  ]
}
```
