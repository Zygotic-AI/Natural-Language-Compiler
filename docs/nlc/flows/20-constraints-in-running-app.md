# Constraints in the running app

**Summary**

Still ahead: constraints become data types enforced in the running application, and a policy change regenerates the units that policy owns.

**Paragraph**

Still ahead, after precise rewrite. The constraint is no longer only a compile-time check. It becomes a data type, and the running application enforces it in the code NLC generated. When the policy changes, precise rewrite regenerates the units that policy owns. You bring the regulation text. A review follows the type back to the constraint on the graph.

**Graph**

```json
{
  "nodes": [
    {
      "id": "codified-constraint",
      "type": "concept",
      "label": "Codified constraint"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    },
    {
      "id": "running-app",
      "type": "system",
      "label": "Running app"
    }
  ],
  "edges": [
    {
      "from": "codified-constraint",
      "to": "produced-code",
      "kind": "constrains"
    },
    {
      "from": "produced-code",
      "to": "running-app",
      "kind": "part_of"
    }
  ]
}
```
