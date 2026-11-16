# Requirement packs

**Summary**

A policy document can be ingested, approved, and installed as a versioned pack that points at what to regenerate.

**Paragraph**

A policy document can be ingested into candidate requirements. You approve them, and the approved set can be exported and installed as a versioned pack. Install then points at what should be regenerated. The pack enters the graph as constraints, and NLC writes the code that carries them. The fuller import, with source page and line on every constraint, is still ahead.

**Graph**

```json
{
  "nodes": [
    {
      "id": "policy-standard-etc",
      "type": "concept",
      "label": "Policy / standard / etc"
    },
    {
      "id": "exact-quote",
      "type": "artifact",
      "label": "Exact quote"
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
      "from": "policy-standard-etc",
      "to": "exact-quote",
      "kind": "extracts_to"
    },
    {
      "from": "exact-quote",
      "to": "requirement-pack",
      "kind": "codifies_as"
    },
    {
      "from": "requirement-pack",
      "to": "produced-code",
      "kind": "constrains"
    }
  ]
}
```
