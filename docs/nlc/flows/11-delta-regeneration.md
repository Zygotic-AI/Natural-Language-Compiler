# Delta regeneration

**Summary**

Changing one requirement queues regeneration of only the code that requirement touches, and each queued step goes through planit.

**Paragraph**

You name the verb, noun, goal, or rule that changed. The impact graph sizes the blast radius, and the tool writes a queue of steps. Each step is a planit run: generate that unit, gate it, then the next. When the queue is done, the tree is proved. You change the decision. The compiler rewrites the affected units. A review of the change is which requirement moved and which code was regenerated from it.

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
      "id": "planit",
      "type": "process-step",
      "label": "PLANIT"
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
      "to": "blast-radius",
      "kind": "requires"
    },
    {
      "from": "blast-radius",
      "to": "impact-graph",
      "kind": "part_of"
    },
    {
      "from": "impact-graph",
      "to": "planit",
      "kind": "allows"
    },
    {
      "from": "planit",
      "to": "produced-code",
      "kind": "produces"
    }
  ]
}
```
