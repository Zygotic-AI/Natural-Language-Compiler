# Public packs

**Summary**

Still ahead: a registered group publishes a signed pack that installs into your graph as constraints the compiler enforces.

**Paragraph**

Still ahead, after other languages. A group registers, confirms an email, and uploads a signed bundle that is checked file by file before it is listed. You install that pack, and it enters the graph as constraints NLC enforces in the codebase it manages. How a stolen signing key is retired, and how a legitimate group rotates a key, has to be solved before this flow ships. The audit follows the signature to the constraints, then the graph to the code.

**Graph**

```json
{
  "nodes": [
    {
      "id": "pack-publisher",
      "type": "concept",
      "label": "Pack publisher"
    },
    {
      "id": "signing-key",
      "type": "artifact",
      "label": "Signing key"
    },
    {
      "id": "requirement-pack",
      "type": "concept",
      "label": "Requirement pack"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    }
  ],
  "edges": [
    {
      "from": "pack-publisher",
      "to": "requirement-pack",
      "kind": "produces"
    },
    {
      "from": "signing-key",
      "to": "requirement-pack",
      "kind": "allows"
    },
    {
      "from": "requirement-pack",
      "to": "produced-code",
      "kind": "constrains"
    }
  ]
}
```
