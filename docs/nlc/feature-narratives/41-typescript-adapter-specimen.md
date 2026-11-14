# TypeScript adapter specimen

**Summary**

A TypeScript specimen shows the shape of an adapter beside the Python path the compiler actually manages.

**Paragraph**

A TypeScript example shows the shape of an adapter beside the Python path. It is a teaching specimen so the idea of another language has a concrete form. The compiler that manages a codebase and audits it through the graph, today, is the Python compiler. Turning a foreign application into another language waits on brownfield and on real language emit.

**Graph**

```json
{
  "nodes": [
    {
      "id": "language-adapter",
      "type": "concept",
      "label": "Language adapter"
    },
    {
      "id": "compiler",
      "type": "system",
      "label": "Compiler"
    },
    {
      "id": "language",
      "type": "concept",
      "label": "Language"
    }
  ],
  "edges": [
    {
      "from": "language-adapter",
      "to": "compiler",
      "kind": "part_of"
    },
    {
      "from": "language-adapter",
      "to": "language",
      "kind": "requires"
    }
  ]
}
```
