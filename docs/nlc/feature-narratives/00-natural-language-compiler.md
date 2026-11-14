# Natural Language Compiler

**Summary**

The Natural Language Compiler turns a plain-language description and its constraints into an application it fully owns, and its graph makes every review of that code automatic.

**Paragraph**

The Natural Language Compiler is a compiler for software. You describe the application in plain language and add the constraints it has to satisfy, from a business rule to a security or compliance standard. NLC turns that intent into the application and keeps the whole codebase. You do not write the code. You approve what the product should do, and NLC generates, updates, and refuses changes that do not match what you accepted.

NLC records the work on an internal graph: each goal, constraint, decision, and the code that carries them are tied together. When a constraint or a technical choice changes, the compiler regenerates the code that decision touches and stops if the result does not match. The codebase stays aligned with the decisions, because NLC is the only path that changes it.

That same graph is what makes review automatic. A code review, a compliance check, or any other review of the code is a query over recorded links: which rule applies, where it is enforced, and which decision put it there. The audit follows those links instead of asking a person to reread the tree. NLC does not supply the regulation texts themselves. You bring those constraints, and the graph is what lets every review of the code run from them.

**Graph**

```json
{
  "nodes": [
    {
      "id": "nlc",
      "type": "product",
      "label": "Natural Language Compiler"
    },
    {
      "id": "interview",
      "type": "process-step",
      "label": "Interview"
    },
    {
      "id": "goal",
      "type": "concept",
      "label": "Goal"
    },
    {
      "id": "accepted-decision",
      "type": "concept",
      "label": "Accepted decision"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    },
    {
      "id": "code-adversarial-audit",
      "type": "process-step",
      "label": "Code adversarial audit"
    }
  ],
  "edges": [
    {
      "from": "interview",
      "to": "goal",
      "kind": "produces"
    },
    {
      "from": "goal",
      "to": "produced-code",
      "kind": "produces_summary"
    },
    {
      "from": "accepted-decision",
      "to": "produced-code",
      "kind": "constrains"
    },
    {
      "from": "produced-code",
      "to": "code-adversarial-audit",
      "kind": "audited_by"
    }
  ]
}
```
