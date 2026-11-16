# Hub release

**Summary**

Maintainers cut a release of the compiler with one command, and the planner walks the version, the checks, the pull request, and the tag.

**Paragraph**

Work stays on a branch, and main moves only when a release pull request merges. The release command takes no version-bump flags. Inside that command the planner picks one version, one release branch, and one tag, and it runs the checks, the notes, and the pull request before the tag is applied to the merge. The checker digest is signed at tag time so the checks that audit a codebase are the checks approved for that compiler. Your application's release stays on the verify-and-ship flow.

**Graph**

```json
{
  "nodes": [
    {
      "id": "ship",
      "type": "process-step",
      "label": "Ship"
    },
    {
      "id": "version-store",
      "type": "concept",
      "label": "Version store"
    },
    {
      "id": "checker-digest",
      "type": "artifact",
      "label": "Checker digest"
    },
    {
      "id": "checker-signature",
      "type": "artifact",
      "label": "Checker signature"
    }
  ],
  "edges": [
    {
      "from": "version-store",
      "to": "checker-digest",
      "kind": "comprises"
    },
    {
      "from": "checker-digest",
      "to": "checker-signature",
      "kind": "produces"
    },
    {
      "from": "ship",
      "to": "checker-signature",
      "kind": "requires"
    }
  ]
}
```
