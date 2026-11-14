# Finished low-code UI

**Summary**

Still ahead, last: a product interface sits on the same path, where you describe the application and NLC writes and reviews the code.

**Paragraph**

Still ahead, last. A product interface sits on the same compile path: you describe the application, you accept the decisions, and NLC writes the codebase and runs every review of that code through the graph. The interface waits until that path is the one we are actually shipping, so the screen is built on the real graph and the real checks.

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
