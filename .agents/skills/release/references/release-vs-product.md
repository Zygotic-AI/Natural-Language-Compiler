# Hub release vs product ship

- **Hub release** = the seven steps of ADR 0061 (`./release validate|sign|main|tag`). Product backlog rows in FINDINGS do not block it; a failing check in `./release validate` does.
- **Product ship** = an adopter's `Released-by:` on `CONFIRM.md`, checked by `tools/release-audit.py`. The agent never writes it.
