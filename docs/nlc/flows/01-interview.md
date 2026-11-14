# Interview

**Summary**

The interview turns a plain-language description into named goals, requirements, and facts, and it stops before any code is written.

**Paragraph**

You describe the application, and the interview loads what already exists before it asks anything new. It names goals, binds facts, and records what you waived. The handoff is a resolution table the compile loop can start from. No code is written in this flow. NLC still owns the codebase, so the interview is how intent enters the graph.

**Graph**

```json
{
  "nodes": [
    {
      "id": "interview",
      "type": "process-step",
      "label": "Interview"
    },
    {
      "id": "goal",
      "type": "concept",
      "label": "Goal"
    },
    {
      "id": "requirement",
      "type": "concept",
      "label": "Requirement"
    },
    {
      "id": "knowledge-fact",
      "type": "concept",
      "label": "Knowledge fact"
    }
  ],
  "edges": [
    {
      "from": "interview",
      "to": "goal",
      "kind": "produces"
    },
    {
      "from": "interview",
      "to": "requirement",
      "kind": "produces"
    },
    {
      "from": "interview",
      "to": "knowledge-fact",
      "kind": "produces"
    }
  ]
}
```
