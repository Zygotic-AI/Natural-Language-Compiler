# Knowledge facts before generate

**Summary**

Generation runs only from facts already bound, and it refuses a stale set.

**Paragraph**

Facts about the system are bound before NLC generates code, and generation refuses to run on a stale set of facts. The compiler writes only from facts you have already established. If those facts are out of date, the build stops. The codebase stays tied to the record, and a review can see which facts were in force when the code was produced.
