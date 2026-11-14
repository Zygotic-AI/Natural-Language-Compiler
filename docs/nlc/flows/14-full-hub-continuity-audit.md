# Full hub continuity audit

**Summary**

The continuity audit checks that beliefs, decisions, requirements, gates, and the product story still agree, using the stage list in the audit manifest.

**Paragraph**

This is the hub's own continuity check, separate from an application's verify. A quick profile is the landmine, a release-prep profile runs while cutting a compiler release, and the full profile includes verify on a clean tree. The stages live in one manifest, and the command lists them rather than copying the list into prose. An agent session runs the machine stages and then an inference checklist. Pass is one line. A failed stage id is the miss.

**Graph**

```json
{
  "nodes": [
    {
      "id": "audit",
      "type": "concept",
      "label": "Audit"
    },
    {
      "id": "requirement",
      "type": "concept",
      "label": "Requirement"
    },
    {
      "id": "gate",
      "type": "concept",
      "label": "Gate"
    },
    {
      "id": "verify",
      "type": "process-step",
      "label": "Verify"
    }
  ],
  "edges": [
    {
      "from": "requirement",
      "to": "gate",
      "kind": "requires"
    },
    {
      "from": "gate",
      "to": "verify",
      "kind": "allows"
    },
    {
      "from": "verify",
      "to": "audit",
      "kind": "audited_by"
    }
  ]
}
```
