# Full requirement import

**Summary**

Still ahead: a policy becomes accepted goals and constraints that each cite source, page, and line.

**Paragraph**

Still ahead. A policy or standard becomes accepted goals and if-then constraints, each one citing the source, the page, and the line. You edit and approve. The compiler writes one chunk per pass and stops. Interview remains the path when there is no source document. This is the full job behind today's pack ingest, and it comes first among the remaining work because the trace graph needs real imported constraints to point at. NLC still writes the code. The import is how those constraints become precise enough for every later audit.

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
