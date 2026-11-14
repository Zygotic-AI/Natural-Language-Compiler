# Python call-tree inventory

**Summary**

For Python, NLC records the path from each verb down to the functions in the domain code.

**Paragraph**

For Python, NLC inventories the path from each verb down to the functions inside the domain code. That inventory is part of the graph for the language the compiler manages today. A review can see which interior functions a goal reaches, because the compiler recorded the tree while it owned the code.

**Graph**

```json
{
  "nodes": [
    {
      "id": "verb-on-noun",
      "type": "concept",
      "label": "Verb (on noun)"
    },
    {
      "id": "interior-function",
      "type": "concept",
      "label": "Interior function"
    }
  ],
  "edges": [
    {
      "from": "verb-on-noun",
      "to": "interior-function",
      "kind": "comprises"
    }
  ]
}
```
