# Brownfield inventory (beta)

**Summary**

An existing repository can be inventoried and partly applied, and this beta still asks you to add one noun and one goal by hand.

**Paragraph**

An existing repository can be inventoried, planned, and partly applied, so NLC can start taking over a codebase it did not originally write. This beta still asks you to add one noun and one goal by hand. The graph begins to cover that tree, and the automated review covers the part the compiler has taken. The full migration, with no special case for a familiar repository, is later work.

**Graph**

```json
{
  "nodes": [
    {
      "id": "brownfield-inventory",
      "type": "process-step",
      "label": "Brownfield inventory"
    },
    {
      "id": "noun",
      "type": "concept",
      "label": "Noun"
    },
    {
      "id": "goal",
      "type": "concept",
      "label": "Goal"
    }
  ],
  "edges": [
    {
      "from": "brownfield-inventory",
      "to": "noun",
      "kind": "allows"
    },
    {
      "from": "brownfield-inventory",
      "to": "goal",
      "kind": "allows"
    }
  ]
}
```
