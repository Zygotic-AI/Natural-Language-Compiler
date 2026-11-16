# Language inventory scan

**Summary**

NLC lists the languages present in a repository, and that list is an inventory.

**Paragraph**

NLC lists the languages present in a repository. The list is an inventory of what is in the tree. Python is the language the compiler compiles and audits end to end. The scan tells a review which parts of the codebase are already on that path and which languages are only identified so far.

**Graph**

```json
{
  "nodes": [
    {
      "id": "compiled-system",
      "type": "system",
      "label": "Compiled system"
    },
    {
      "id": "language",
      "type": "concept",
      "label": "Language"
    }
  ],
  "edges": [
    {
      "from": "compiled-system",
      "to": "language",
      "kind": "comprises"
    }
  ]
}
```
