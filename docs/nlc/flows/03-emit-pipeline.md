# Emit pipeline

**Summary**

Nothing is emitted until the action is on the plan and the applicable decisions are bound, and every emit is audited before the next one starts.

**Paragraph**

The pipeline runs inside planit around each emit. First the action has to map to a plan step, and every applicable accepted decision has to be bound to an action. Then the compiler writes the artifact and a manifest. After that, the emit must have an audit, the manifest must match its schema, and the gates of the bound decisions must pass. A miss stops the run. The files that land in the tree are the ones this sequence allowed, so a review can follow the plan step to the code.

**Graph**

```json
{
  "nodes": [
    {
      "id": "atomic-action",
      "type": "process-step",
      "label": "Atomic action"
    },
    {
      "id": "constraint-bind",
      "type": "process-step",
      "label": "Constraint bind"
    },
    {
      "id": "reverse-adversarial-audit",
      "type": "process-step",
      "label": "Reverse adversarial audit"
    },
    {
      "id": "emit",
      "type": "process-step",
      "label": "Emit"
    },
    {
      "id": "artifact-manifest",
      "type": "artifact",
      "label": "Artifact manifest"
    },
    {
      "id": "audit",
      "type": "concept",
      "label": "Audit"
    }
  ],
  "edges": [
    {
      "from": "atomic-action",
      "to": "constraint-bind",
      "kind": "precedes"
    },
    {
      "from": "constraint-bind",
      "to": "reverse-adversarial-audit",
      "kind": "precedes"
    },
    {
      "from": "reverse-adversarial-audit",
      "to": "emit",
      "kind": "allows"
    },
    {
      "from": "emit",
      "to": "artifact-manifest",
      "kind": "produces"
    },
    {
      "from": "artifact-manifest",
      "to": "audit",
      "kind": "audited_by"
    }
  ]
}
```
