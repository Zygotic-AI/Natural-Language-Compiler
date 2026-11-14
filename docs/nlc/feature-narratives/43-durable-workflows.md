# Durable workflows with tagged engines

**Summary**

A durable goal is bound to a named engine, and a bad pairing fails.

**Paragraph**

A goal that must run as a durable workflow is bound to a named engine. A bad pairing fails. NLC writes that binding into the codebase it manages, and the checks reject an engine that does not match the goal. A review of the workflow is a review of that binding on the graph, not a separate stack beside the code.

**Graph**

```json
{
  "nodes": [
    {
      "id": "workflow",
      "type": "concept",
      "label": "Workflow"
    },
    {
      "id": "durable-engine",
      "type": "concept",
      "label": "Durable engine"
    }
  ],
  "edges": [
    {
      "from": "workflow",
      "to": "durable-engine",
      "kind": "requires"
    }
  ]
}
```
