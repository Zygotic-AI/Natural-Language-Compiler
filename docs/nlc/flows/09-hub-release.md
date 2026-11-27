# Hub release

**Summary**

Maintainers cut a compiler release by running the release goal. Readiness is the checklist in [ADR 0061](../../../adrs/0061-release-in-seven-steps.md). This page explains; it does not copy the steps.

**Paragraph**

Work stays on a release line. `main` moves only when the release goal pushes a signed tree. The first check is whether this milestone’s issues are completed. The owner signs the release once, after validate. The tag is production.

**Graph**

```json
{
  "nodes": [
    {
      "id": "release-goal",
      "type": "process-step",
      "label": "Release goal"
    },
    {
      "id": "readiness",
      "type": "artifact",
      "label": "ADR 0061 checklist"
    },
    {
      "id": "milestone-issues",
      "type": "artifact",
      "label": "Milestone issues"
    }
  ],
  "edges": [
    {
      "from": "milestone-issues",
      "to": "readiness",
      "kind": "requires"
    },
    {
      "from": "readiness",
      "to": "release-goal",
      "kind": "requires"
    }
  ]
}
```
