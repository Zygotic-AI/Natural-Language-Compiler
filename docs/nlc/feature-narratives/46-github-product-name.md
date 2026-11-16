# GitHub product name

**Summary**

The compiler is installed from Zygotic-AI/Natural-Language-Compiler.

**Paragraph**

The compiler is installed from Zygotic-AI/Natural-Language-Compiler. That repository is the public identity of the product that manages your codebase and runs the audits over its graph. What you install is a tagged compiler from that repository.

**Graph**

```json
{
  "nodes": [
    {
      "id": "compiler",
      "type": "system",
      "label": "Compiler"
    },
    {
      "id": "nlc",
      "type": "product",
      "label": "Natural Language Compiler"
    },
    {
      "id": "hub",
      "type": "system",
      "label": "Hub"
    }
  ],
  "edges": [
    {
      "from": "compiler",
      "to": "nlc",
      "kind": "part_of"
    },
    {
      "from": "hub",
      "to": "nlc",
      "kind": "part_of"
    }
  ]
}
```
