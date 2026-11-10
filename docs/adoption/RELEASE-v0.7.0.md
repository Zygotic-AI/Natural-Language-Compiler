# Natural Language Compiler hub v0.7.0

## Highlights

Hub **v0.7.0** is a minor on **v0.6.0**.

- **Install into a specific repo (ADR 0060).** The installer asks **global** (this user) or **local** (this git repo). A local pin writes `<repo>/.nlc` and is not dragged along when the machine-wide install moves. Piped `curl | bash` stays global unless `--local` / `NLC_INSTALL_SCOPE=local`.
- **PATH `nlc` dispatches to the repo copy.** If the command on PATH is the global shim and the current repo has `./nlc`, it execs that copy and passes every argument through.
- **Foreign skills no longer fail install.** Hub skill-author grading uses a hub-only staging copy, then overlays. Skills already in `~/.agents/skills` (including a symlink dest) do not fail the install (GitHub issue 67).

## Changes since v0.6.0

- Install NLC into the current repo (global or local) (#69) (`10d9de4`)
- Revert "Merge pull request #64 from Zygotic-AI/cursor/fresh-base-guard-e01a" (`8e9ce36`)
- fix: sync hub-content-tree-hash and before-generate stamp (`1679133`)
- fix: git identity in deploy guard temp-repo tests (`238be9d`)
- ci: fresh-base PR guard and deploy git guard (`67cf235`)

### Diff stat

```
.gitignore                                         |   5 +
 .nlc/before-generate-stamp.json                    |   4 +-
 DESCRIBE.md                                        |   2 +
 README.md                                          |   4 +-
 TODO                                               |  10 +-
 adrs/0060-install-scope-and-path-dispatch.md       |  58 ++++++++
 adrs/ACTIVE.md                                     |   1 +
 adrs/CATALOG.md                                    |   1 +
 adrs/INDEX.md                                      |   1 +
 adrs/README.md                                     |   1 +
 docs/ADR-ENFORCEMENT.md                            |   1 +
 docs/JOBS-TO-BE-DONE.md                            |   8 +-
 docs/TERMS.md                                      |   4 +-
 docs/adoption/BOOTSTRAP.md                         |   6 +-
 docs/nlc/FEATURES.md                               |  19 +--
 docs/nlc/compiler/GETTING-STARTED.md               |   2 +
 goals/hub_install/execute.ps1                      | 154 ++++++++++++++++----
 goals/hub_install/execute.sh                       | 158 ++++++++++++++++++---
 integrity/adr-gates.json                           |   4 +
 integrity/check-inputs.json                        |  48 +++++++
 integrity/checker-digest.sha256                    |   2 +-
 integrity/gate-set-baseline.manifest.sha256        | 111 ++++++++++-----
 integrity/hub-content-tree-hash.txt                |   2 +-
 integrity/mandated-paths.json                      | 136 ++++++++++++++++++
 integrity/nlc-install-hashes.json                  |   1 +
 scripts/nlc-launcher.cmd                           |  63 ++++++++
 scripts/nlc-launcher.sh                            |  63 ++++++++
 templates/adopter/nlc                              |  24 +++-
 templates/adopter/nlc.cmd                          |  43 ++++--
 tools/README.md                                    |   2 +-
 tools/assert-install-foreign-skills-passes.py      |  12 ++
 tools/assert-install-local-dispatch-passes.py      |  12 ++
 tools/assert-install-local-outside-repo-fails.py   |  12 ++
 tools/assert-install-local-pin-passes.py           |  12 ++
 tools/fitness-install-scope.py                     |  12 ++
 tools/nlc-launch.py                                |  12 ++
 .../assert_install_foreign_skills_passes/README.md |   3 +
 .../__init__.py                                    |   2 +
 .../adjectives.txt                                 |   1 +
 .../assert_install_foreign_skills_passes.py        | 117 +++++++++++++++
 .../fields.txt                                     |   1 +
 .../schemas/verbs.schema.json                      |  10 ++
 .../assert_install_local_dispatch_passes/README.md |   3 +
 .../__init__.py                                    |   2 +
 .../adjectives.txt                                 |   1 +
 .../assert_install_local_dispatch_passes.py        |  70 +++++++++
 .../fields.txt                                     |   1 +
 .../schemas/verbs.schema.json                      |  10 ++
 .../README.md                                      |   3 +
 .../__init__.py                                    |   2 +
 .../adjectives.txt                                 |   1 +
 .../assert_install_local_outside_repo_fails.py     |  52 +++++++
 .../fields.txt                                     |   1 +
 .../schemas/verbs.schema.json                      |  10 ++
 .../assert_install_local_pin_passes/README.md      |   3 +
 .../assert_install_local_pin_passes/__init__.py    |   2 +
 .../assert_install_local_pin_passes/adjectives.txt |   1 +
 .../assert_install_local_pin_passes.py             |  78 ++++++++++
 .../assert_install_local_pin_passes/fields.txt     |   1 +
 .../schemas/verbs.schema.json                      |  10 ++
 .../assert_project_lock_schema_passes.py           |  32 ++++-
 tools/nouns/ci_fitness/ci_fitness.py               |  20 +++
 tools/nouns/cli_help/cli_help.py                   |   6 +-
 .../fitness_distribution_binder.py                 |   4 +
 tools/nouns/fitness_install_scope/README.md        |   3 +
 tools/nouns/fitness_install_scope/__init__.py      |   2 +
 tools/nouns/fitness_install_scope/adjectives.txt   |   1 +
 tools/nouns/fitness_install_scope/fields.txt       |   1 +
 .../fitness_install_scope/fitness_install_scope.py |  77 ++++++++++
 .../schemas/verbs.schema.json                      |  10 ++
 tools/nouns/lock_validate/lock_validate.py         |  10 +-
 tools/nouns/nlc_distribution/nlc_distribution.py   |   5 +-
 tools/nouns/nlc_hub_cli/nlc_hub_cli.py             |  24 +++-
 tools/nouns/nlc_init/nlc_init.py                   |  22 ++-
 tools/nouns/nlc_launch/README.md                   |   3 +
 tools/nouns/nlc_launch/__init__.py                 |   2 +
 tools/nouns/nlc_launch/adjectives.txt              |   1 +
 tools/nouns/nlc_launch/fields.txt                  |   1 +
 tools/nouns/nlc_launch/nlc_launch.py               | 106 ++++++++++++++
 tools/nouns/nlc_launch/schemas/verbs.schema.json   |  10 ++
 80 files changed, 1606 insertions(+), 129 deletions(-)
```

