# Python-first compiled systems

**Summary**

Python is the language NLC compiles, gates, and audits end to end today.

**Paragraph**

Applications in Python are what NLC compiles and gates today. The compiler manages that codebase end to end: it writes the code, records it on the graph, and runs the automated review. Other languages can be listed. Equal support for them is later work.

**Graph**

```json
{
  "nodes": [
    {
      "id": "emit",
      "type": "process-step",
      "label": "Emit"
    },
    {
      "id": "language",
      "type": "concept",
      "label": "Language"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    },
    {
      "id": "language-adapter",
      "type": "concept",
      "label": "Language adapter"
    },
    {
      "id": "compiler",
      "type": "system",
      "label": "Compiler"
    }
  ],
  "edges": [
    {
      "from": "emit",
      "to": "language",
      "kind": "requires"
    },
    {
      "from": "emit",
      "to": "produced-code",
      "kind": "produces"
    },
    {
      "from": "language-adapter",
      "to": "compiler",
      "kind": "part_of"
    }
  ]
}
```
