# Constraints as data types in the running app

**Summary**

Still ahead: constraints become data types enforced in the running application, and a policy change regenerates the units that policy owns.

**Paragraph**

Still ahead, after precise rewrite. Constraints become data types and are enforced by code in the running application, not only when the compiler checks the tree. When the policy changes, precise rewrite regenerates the units that policy owns. You bring the regulation text. NLC puts the enforcement into the application it manages, and a review follows the type back to the constraint on the graph.

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
