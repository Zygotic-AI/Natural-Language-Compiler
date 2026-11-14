# Quality as pass or fail

**Summary**

Every gate is pass or fail, so a review does not grade a percentage.

**Paragraph**

Every gate is pass or fail. The automated audit of the codebase is binary, so a review does not grade a percentage. If the graph, the rules, or the generated files do not match, the step fails and NLC stops. The code that remains is code that passed.

**Graph**

```json
{
  "nodes": [
    {
      "id": "gate",
      "type": "concept",
      "label": "Gate"
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
    }
  ],
  "edges": [
    {
      "from": "gate",
      "to": "emit",
      "kind": "allows"
    },
    {
      "from": "gate",
      "to": "verify",
      "kind": "allows"
    }
  ]
}
```
