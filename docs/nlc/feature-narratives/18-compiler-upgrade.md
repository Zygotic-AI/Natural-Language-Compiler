# Compiler upgrade

Upgrade walks an application from one pinned compiler version to the next along the version chain. The lock changes because you ran the upgrade. The codebase is then regenerated and checked under the new compiler, still with NLC writing the code and the graph recording what changed.
