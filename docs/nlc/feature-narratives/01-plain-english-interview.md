# Plain-English interview

**Summary**

The interview turns what you say into named goals, requirements, and facts, and it stops before any code is written.

**Paragraph**

You start by describing the application in ordinary language. The interview splits that description into named goals, requirements, and facts, and it stops there. No code is written until those pieces are named and you have accepted them. This is the front door for intent. From here, NLC manages the codebase, so a conversation does not quietly become source files.

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
