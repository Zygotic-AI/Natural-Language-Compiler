# Other languages

**Summary**

Still ahead: NLC emits and checks languages other than Python, and still owns the codebase.

**Paragraph**

Still ahead, after self-brownfield. A team keeps the language it already uses. The compiler emits and checks that language, the graph still drives the audits, and a foreign application changes language by being taken over and then re-emitted. Public sharing of packs waits on this, because teams arrive when their language is actually managed by NLC.

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
      "id": "brownfield-inventory",
      "type": "process-step",
      "label": "Brownfield inventory"
    }
  ],
  "edges": [
    {
      "from": "brownfield-inventory",
      "to": "emit",
      "kind": "allows"
    },
    {
      "from": "emit",
      "to": "language",
      "kind": "requires"
    },
    {
      "from": "emit",
      "to": "produced-code",
      "kind": "produces"
    }
  ]
}
```
