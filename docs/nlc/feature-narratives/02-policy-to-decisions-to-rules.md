# Policy to decisions to rules

**Summary**

A policy or standard becomes an accepted decision and then if-then rules the compiler applies when it writes the code.

**Paragraph**

Constraints you care about, a company policy or a technical standard, become accepted decisions and then if-then rules the compiler can run. You approve the decision. NLC applies the rule when it writes the code, so the constraint is in the codebase because the compiler put it there. A later review can ask where that rule is enforced and follow the link, instead of reading the tree by hand.

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
      "id": "accepted-decision",
      "type": "concept",
      "label": "Accepted decision"
    },
    {
      "id": "rule",
      "type": "concept",
      "label": "Rule"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
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
      "from": "accepted-decision",
      "to": "rule",
      "kind": "codifies_as"
    },
    {
      "from": "rule",
      "to": "codified-constraint",
      "kind": "precedes"
    },
    {
      "from": "codified-constraint",
      "to": "produced-code",
      "kind": "constrains"
    }
  ]
}
```
