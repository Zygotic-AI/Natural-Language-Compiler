# RCA

**Summary**

A non-trivial compile failure is recorded as a process miss, and the fix goes back into the interview or the decision before the compiler regenerates.

**Paragraph**

When planit fails and the miss is not trivial, the run stops and a packet records which decision, rule, or step was wrong. The packet names the process, and the schema check refuses a packet that blames a person. The flow then returns to the interview or to binding, and generation runs again from the corrected record. The concept graph links the audit to the packet and the packet back to the interview, which is this return path.

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
      "id": "rca-packet",
      "type": "artifact",
      "label": "RCA packet"
    },
    {
      "id": "interview",
      "type": "process-step",
      "label": "Interview"
    },
    {
      "id": "planit",
      "type": "process-step",
      "label": "PLANIT"
    }
  ],
  "edges": [
    {
      "from": "audit",
      "to": "rca-packet",
      "kind": "produces"
    },
    {
      "from": "rca-packet",
      "to": "interview",
      "kind": "allows"
    },
    {
      "from": "interview",
      "to": "planit",
      "kind": "allows"
    }
  ]
}
```
