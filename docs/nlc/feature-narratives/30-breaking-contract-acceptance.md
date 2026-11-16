# Breaking-contract acceptance

**Summary**

A contract break stays failed until you accept the requirement that allows it, and the compiler lists the callers it affects.

**Paragraph**

If a change breaks a contract, the build stays failed until you accept the requirement that allows the break. The compiler keeps the list of callers the break affects. You accept the new requirement, and only then does NLC regenerate the codebase around it. The audit shows the acceptance and the callers, because both are on the record.

**Graph**

```json
{
  "nodes": [
    {
      "id": "contract",
      "type": "concept",
      "label": "Contract"
    },
    {
      "id": "requirement",
      "type": "concept",
      "label": "Requirement"
    },
    {
      "id": "produced-code",
      "type": "artifact",
      "label": "Produced code"
    }
  ],
  "edges": [
    {
      "from": "contract",
      "to": "produced-code",
      "kind": "constrains"
    },
    {
      "from": "requirement",
      "to": "contract",
      "kind": "requires"
    }
  ]
}
```
