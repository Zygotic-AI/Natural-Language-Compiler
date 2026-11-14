# Retry idempotency checks

**Summary**

A retry that would apply the same change twice fails the check.

**Paragraph**

A retry that would apply the same change twice fails the check. The compiler can run a step again without doubling the effect in the codebase. When the graph says a unit must be regenerated, the second run does not stack a second copy of the change on the first, and the audit still describes one change.
