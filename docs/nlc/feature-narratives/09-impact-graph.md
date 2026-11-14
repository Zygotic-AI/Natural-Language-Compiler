# Impact graph

**Summary**

The Impact graph holds each Goal and the Verb (on noun) that Goal calls.

**Paragraph**

The Impact graph records which Goal calls which Verb (on noun). The Goal and the Verb (on noun) are both part of the Impact graph. You start at the Goal and follow that link to the Verb (on noun).

**Graph**

```json
{
  "nodes": [
    {
      "id": "impact-graph",
      "type": "concept",
      "label": "Impact graph"
    },
    {
      "id": "goal",
      "type": "concept",
      "label": "Goal"
    },
    {
      "id": "verb-on-noun",
      "type": "concept",
      "label": "Verb (on noun)"
    }
  ],
  "edges": [
    {
      "from": "goal",
      "to": "impact-graph",
      "kind": "part_of"
    },
    {
      "from": "verb-on-noun",
      "to": "impact-graph",
      "kind": "part_of"
    }
  ]
}
```
