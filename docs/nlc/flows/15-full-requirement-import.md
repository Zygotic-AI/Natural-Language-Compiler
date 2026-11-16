# Full requirement import

**Summary**

Still ahead: a policy becomes accepted goals and constraints that each cite source, page, and line, one chunk at a time.

**Paragraph**

Still ahead. This is the full job behind today's pack ingest. A source document becomes goals and if-then constraints, each one citing the page and the line, and you edit and approve each chunk before the next is written. Interview remains the path when there is no source document. The trace graph needs these cited constraints to point at. NLC still writes the code. The import is how those constraints become precise enough for every later audit.

**Graph**

```json
{
  "nodes": [
    {
      "id": "policy-standard-etc",
      "type": "concept",
      "label": "Policy / standard / etc"
    },
    {
      "id": "exact-quote",
      "type": "artifact",
      "label": "Exact quote"
    },
    {
      "id": "codified-constraint",
      "type": "concept",
      "label": "Codified constraint"
    },
    {
      "id": "goal",
      "type": "concept",
      "label": "Goal"
    }
  ],
  "edges": [
    {
      "from": "policy-standard-etc",
      "to": "exact-quote",
      "kind": "extracts_to"
    },
    {
      "from": "exact-quote",
      "to": "codified-constraint",
      "kind": "codifies_as"
    },
    {
      "from": "codified-constraint",
      "to": "goal",
      "kind": "constrains"
    }
  ]
}
```
