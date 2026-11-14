# Constraint chain

**Summary**

A policy becomes an exact quote, then a constraint, and an accepted decision becomes a rule the compiler can apply.

**Paragraph**

The source document yields a quote that cites where the words came from. That quote is codified into a constraint the compiler can bind to an action. Separately, an accepted decision becomes an if-then rule, and that rule is the form used at bind time. You approve the decision. NLC writes the code that carries the rule. A later audit follows the quote or the decision to the code, which is the relationship the concept graph already draws.

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
      "id": "adr",
      "type": "concept",
      "label": "ADR"
    },
    {
      "id": "rule",
      "type": "concept",
      "label": "Rule"
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
      "from": "adr",
      "to": "rule",
      "kind": "codifies_as"
    },
    {
      "from": "rule",
      "to": "codified-constraint",
      "kind": "precedes"
    }
  ]
}
```
