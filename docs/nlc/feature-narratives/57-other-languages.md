# Other languages besides Python

**Summary**

Still ahead: NLC emits and checks languages other than Python, and still owns the codebase.

**Paragraph**

Still ahead, after self-brownfield. NLC emits and checks languages other than Python, so a team can keep the language it already uses. The compiler still owns the codebase and the graph still drives the audits. A foreign application changes language by being taken over and then re-emitted. Public sharing of packs waits on this, because teams arrive when their language is actually managed by NLC.

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
