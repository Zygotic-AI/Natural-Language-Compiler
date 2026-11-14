# Gate after every generate

**Summary**

Each generated piece is checked and receipted before the next piece starts.

**Paragraph**

After each piece is generated, that piece is checked before the next piece starts. The check leaves a receipt. If the receipt is missing, verify fails. NLC reviews the code as it is produced, one unit at a time, so the automated audit is part of writing the codebase and not a separate pass someone might skip.
