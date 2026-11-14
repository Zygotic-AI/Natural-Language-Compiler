# Incremental compile

**Summary**

NLC compiles one bound goal at a time and stops when a check fails.

**Paragraph**

NLC compiles one bound goal at a time and stops when a check fails. Each step is small enough that a defect shows up at compile time, in the unit that just changed. You do not write that unit. The compiler does, and the graph records the goal the unit belongs to so a review can start from the goal and land on the code.
