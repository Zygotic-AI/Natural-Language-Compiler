# Trace graph

**Summary**

Still ahead: the trace graph ties goals, actions, constraints, and code by ids so every review is a query over recorded links.

**Paragraph**

Still ahead, after full requirement import. The trace graph ties the compile chain together by ids: a goal splits into atomic actions, those actions bind to constraints, a reverse check confirms applicable constraints were included, the compiler emits each action, and a further check confirms the constraints landed in the code. One graph answers where a policy is enforced by walking only links that were recorded. Code review, compliance review, and every other review of the code run as queries on that graph. NLC still manages the codebase the queries land on. Today's impact graph is the smaller map this extends.

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
      "id": "constraint-bind",
      "type": "process-step",
      "label": "Constraint bind"
    },
    {
      "id": "reverse-adversarial-audit",
      "type": "process-step",
      "label": "Reverse adversarial audit"
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
    },
    {
      "id": "code-adversarial-audit",
      "type": "process-step",
      "label": "Code adversarial audit"
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
      "to": "constraint-bind",
      "kind": "precedes"
    },
    {
      "from": "constraint-bind",
      "to": "reverse-adversarial-audit",
      "kind": "precedes"
    },
    {
      "from": "reverse-adversarial-audit",
      "to": "emit",
      "kind": "allows"
    },
    {
      "from": "emit",
      "to": "produced-code",
      "kind": "produces"
    },
    {
      "from": "produced-code",
      "to": "code-adversarial-audit",
      "kind": "audited_by"
    }
  ]
}
```
