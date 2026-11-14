# Brownfield beta

**Summary**

An existing repository is adopted by inventory and a first noun and goal, with you still adding that noun and goal by hand.

**Paragraph**

This is the beta path for a tree NLC did not originally write. You do not scaffold over existing domain code. You bring the charter and the checks across, then introduce one noun and one goal behind gates before migrating the rest. Contract changes after that use the regeneration queue. The graph begins to cover the part the compiler has taken. The full takeover, with no special case and no hand-added goal, is a later flow.

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
