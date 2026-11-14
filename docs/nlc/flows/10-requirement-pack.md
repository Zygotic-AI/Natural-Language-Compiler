# Requirement pack

**Summary**

A policy document is ingested into candidates, you ratify them, and the result is exported and installed as a versioned pack that points at what to regenerate.

**Paragraph**

Ingest turns a source into candidate decisions and rules, and it stops for a person to ratify them. Export writes a versioned bundle. Install in an application records what the pack covers and hints at the regeneration queue. When a local allow-list has entries, install stays inside that list. The pack then enters the graph as constraints, and NLC writes the code that carries them. The fuller import, with source page and line on every constraint, is the later flow.

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
      "id": "pack-allow-list",
      "type": "concept",
      "label": "Pack allow-list"
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
      "from": "pack-allow-list",
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
