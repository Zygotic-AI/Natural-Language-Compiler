# No editor hooks

**Summary**

The same compile rules apply in every harness, and verify fails if compiled files appear without stamps and gates.

**Paragraph**

NLC does not attach itself to one editor. The same compile rules apply no matter which agent wrote the files. Verify fails if compiled files showed up without the stamps and gates. The compiler's audit of the tree is the review that counts, on the codebase NLC is responsible for.
