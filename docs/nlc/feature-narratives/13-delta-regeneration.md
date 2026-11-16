# Delta regeneration

**Summary**

Changing one requirement queues regeneration of only the code that requirement touches.

**Paragraph**

When one requirement changes, NLC queues regeneration for the code that requirement touches. The impact graph sizes that blast radius. You change the decision, and the compiler rewrites the affected units. A review of the change is the same graph query: which requirement moved, and which code was regenerated from it.

**Graph**

```json
{
  "nodes": [
    {
      "id": "rule",
      "type": "concept",
      "label": "Rule"
    },
    {
      "id": "impact-graph",
      "type": "concept",
      "label": "Impact graph"
    },
    {
      "id": "blast-radius",
      "type": "concept",
      "label": "Blast radius"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    }
  ],
  "edges": [
    {
      "from": "rule",
      "to": "produced-code",
      "kind": "constrains"
    },
    {
      "from": "blast-radius",
      "to": "impact-graph",
      "kind": "part_of"
    },
    {
      "from": "impact-graph",
      "to": "produced-code",
      "kind": "requires"
    }
  ]
}
```
