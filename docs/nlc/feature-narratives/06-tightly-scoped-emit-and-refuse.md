# Tightly scoped emit and refuse

**Summary**

Each step emits only its own code, and a failed check refuses the output.

**Paragraph**

Each compile step emits only the code that step is responsible for. If the checks fail, NLC refuses the output. You do not edit generated files to force a pass. The compiler keeps the whole codebase, and a bad step stops before it becomes the product a review would have to untangle later.
