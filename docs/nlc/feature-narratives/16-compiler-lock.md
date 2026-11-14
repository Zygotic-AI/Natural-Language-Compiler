# Compiler lock

Each application repository is pinned to one version of NLC. Moving that pin is a choice for that repository. The lock keeps the graph, the checks, and the generated code on the same compiler, so an audit of the codebase is an audit against a known compiler and not a moving one.
