# Trace graph run

**Summary**

Still ahead: a recorded run ties goals, actions, constraints, and code by ids so every review is a query over links that were actually written.

**Paragraph**

Still ahead, after full requirement import. The compile spine is the shape of this flow. A recorded run gives each hop an id: the goal, the atomic action, the constraint, the emit, and the code audit. One graph answers where a policy is enforced by walking only those recorded links. Code review and compliance review are that query. NLC still manages the codebase the query lands on. Today's impact graph is the smaller map this extends.

**Graph**

```json
{
  "nodes": [
    {
      "id": "trace-graph",
      "type": "concept",
      "label": "Trace graph"
    },
    {
      "id": "goal",
      "type": "concept",
      "label": "Goal"
    },
    {
      "id": "atomic-action",
      "type": "process-step",
      "label": "Atomic action"
    },
    {
      "id": "codified-constraint",
      "type": "concept",
      "label": "Codified constraint"
    },
    {
      "id": "emit",
      "type": "process-step",
      "label": "Emit"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    }
  ],
  "edges": [
    {
      "from": "goal",
      "to": "trace-graph",
      "kind": "part_of"
    },
    {
      "from": "goal",
      "to": "atomic-action",
      "kind": "comprises"
    },
    {
      "from": "atomic-action",
      "to": "codified-constraint",
      "kind": "binds"
    },
    {
      "from": "emit",
      "to": "produced-code",
      "kind": "produces"
    },
    {
      "from": "produced-code",
      "to": "trace-graph",
      "kind": "part_of"
    }
  ]
}
```
