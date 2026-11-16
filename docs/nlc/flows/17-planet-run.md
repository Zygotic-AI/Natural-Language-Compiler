# Planet run

**Summary**

Still ahead: every artifact of a run carries a manifest, the run keeps one index of those manifests, and the audit reads the manifest with the work.

**Paragraph**

Still ahead, after the trace graph has ids to hang on. Emit produces the work and a manifest. The audit reads both. A run-level index collects the manifests, and each model call records the model, the provider, the harness, the tokens, and the cost when the model returns it. Failure records get the same treatment. The graph can then reconstruct how the codebase was produced, not only the final files.

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
      "id": "artifact-manifest",
      "type": "artifact",
      "label": "Artifact manifest"
    },
    {
      "id": "audit",
      "type": "concept",
      "label": "Audit"
    },
    {
      "id": "run-level-index",
      "type": "artifact",
      "label": "Run-level index"
    },
    {
      "id": "model-call-record",
      "type": "artifact",
      "label": "Model-call record"
    }
  ],
  "edges": [
    {
      "from": "emit",
      "to": "artifact-manifest",
      "kind": "produces"
    },
    {
      "from": "artifact-manifest",
      "to": "audit",
      "kind": "audited_by"
    },
    {
      "from": "run-level-index",
      "to": "artifact-manifest",
      "kind": "comprises"
    },
    {
      "from": "run-level-index",
      "to": "model-call-record",
      "kind": "comprises"
    }
  ]
}
```
