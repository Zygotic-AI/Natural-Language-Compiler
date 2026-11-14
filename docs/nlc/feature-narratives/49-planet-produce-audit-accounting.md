# Planet produce / audit accounting

**Summary**

Still ahead: every produced artifact carries a manifest, and each run records the decisions, model calls, and audits that created the code.

**Paragraph**

Still ahead, after the trace graph has ids to hang on. Everything NLC produces is followed by an audit, and every artifact carries a manifest the audit reads beside the work itself. A run collects those manifests in one index. Decisions about which accepted rules applied are written into that record. Each model call records the model, the provider, the harness, the tokens, and the cost when the model returns it. Failure records and the other steps that use a model get the same treatment. The graph can then reconstruct a run, not only the final files, so the automated review covers how the codebase was produced.

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
