# Natural Language Compiler hub v0.8.0

## Highlights

Hub **v0.8.0** is a minor on **v0.7.0**.

- **Lazy-load skills at install.** On an interactive terminal the installer asks `Lazy-load skills (disable-model-invocation)? y/N`. Enter, `n`, or any other answer writes `disable-model-invocation: false` on the skills this install copies. `y` or `yes` writes `true`. Piped install and CI do not ask and write `false`. Skills already in the folder that this install did not copy stay as they are.
- **Product story pack.** Feature narratives, operator flows, and the concept graph for the released and upcoming story are in this line.

## Changes since v0.7.0

- feat(install): ask whether to lazy-load skills (`e804c1f`)
- save: saving x6 (`34cde22`)
- save: saving x5 (`642ec9c`)
- save: saving x4 (`f4f50c0`)
- save: saving x3 (`a3dedf4`)
- save: saving x2 (`dd57a3e`)
- Add FEATURES-DRAFT-NOVEMBER.md: Planet tenets, observability/traceability additions, RCA manifest requirement (`1952b8b`)

### Diff stat

```
.nlc/gate-records.json                             |  14 +
 .nlc/gate-scope.json                               |   2 +
 .nlc/plan-audit-export-features-audit-plan.json    |  58 +++
 .nlc/plan-audit-export-features-fold.json          |  54 ++
 .nlc/plan-audit.json                               |  66 +--
 .nlc/work-queue.json                               |   7 +
 DESCRIBE.md                                        |   8 +-
 docs/adoption/BOOTSTRAP.md                         |   2 +-
 docs/diagrams/filter-concept-graph-edges.mjs       |  48 ++
 docs/diagrams/nlc-concept-graph-spine.json         | 366 ++++++++++++++
 docs/diagrams/nlc-concept-graph-spine.md           |  22 +
 docs/nlc/FEATURES-AUDIT-PLAN.md                    | 122 +++++
 docs/nlc/FEATURES-AUDIT-REGISTER.md                | 206 ++++++++
 docs/nlc/FEATURES-DRAFT-NOVEMBER.md                |   5 +
 docs/nlc/FEATURES.md                               | 140 +++---
 docs/nlc/README.md                                 |   1 +
 docs/nlc/compiler/GETTING-STARTED.md               |   2 +-
 docs/nlc/concept-graph/README.md                   | 152 ++++++
 docs/nlc/concept-graph/edge-types.json             | 141 ++++++
 docs/nlc/concept-graph/edges.json                  | 500 ++++++++++++++++++
 docs/nlc/concept-graph/nodes.json                  | 556 +++++++++++++++++++++
 .../00-natural-language-compiler.md                |  74 +++
 .../01-plain-english-interview.md                  |  55 ++
 .../02-policy-to-decisions-to-rules.md             |  75 +++
 docs/nlc/feature-narratives/03-decision-log.md     |  55 ++
 .../04-knowledge-facts-before-generate.md          |  65 +++
 .../feature-narratives/05-incremental-compile.md   |  60 +++
 .../06-tightly-scoped-emit-and-refuse.md           |  55 ++
 .../feature-narratives/07-emit-pipeline-gates.md   |  55 ++
 .../08-gate-after-every-generate.md                |  55 ++
 docs/nlc/feature-narratives/09-impact-graph.md     |  45 ++
 docs/nlc/feature-narratives/10-verify-path.md      |  45 ++
 .../feature-narratives/11-adversarial-review.md    |  55 ++
 .../feature-narratives/12-defects-go-upstream.md   |  60 +++
 .../feature-narratives/13-delta-regeneration.md    |  55 ++
 docs/nlc/feature-narratives/14-one-line-install.md |  45 ++
 .../15-checksum-verified-install.md                |  45 ++
 docs/nlc/feature-narratives/16-compiler-lock.md    |  50 ++
 .../17-install-into-a-specific-repo.md             |  50 ++
 docs/nlc/feature-narratives/18-compiler-upgrade.md |  50 ++
 docs/nlc/feature-narratives/19-install-doctor.md   |  45 ++
 .../20-loadable-published-skills.md                |  45 ++
 .../21-greenfield-app-scaffold.md                  |  50 ++
 .../feature-narratives/22-human-cli-dashboard.md   |  45 ++
 .../feature-narratives/23-adopter-ci-template.md   |  45 ++
 .../nlc/feature-narratives/24-requirement-packs.md |  55 ++
 .../feature-narratives/25-hub-local-pack-list.md   |  35 ++
 .../feature-narratives/26-rule-receipts-in-code.md |  45 ++
 docs/nlc/feature-narratives/27-rules-that-fight.md |  55 ++
 .../feature-narratives/28-semantic-rule-apply.md   |  55 ++
 .../feature-narratives/29-closed-set-expansion.md  |  45 ++
 .../30-breaking-contract-acceptance.md             |  45 ++
 docs/nlc/feature-narratives/31-change-class-a-f.md |  45 ++
 .../32-produce-audit-ship-roles.md                 |  55 ++
 docs/nlc/feature-narratives/33-human-ship-check.md |  45 ++
 .../feature-narratives/34-quality-pass-or-fail.md  |  45 ++
 .../nlc/feature-narratives/35-retry-idempotency.md |  35 ++
 docs/nlc/feature-narratives/36-rca-packet.md       |  45 ++
 docs/nlc/feature-narratives/37-no-editor-hooks.md  |  45 ++
 docs/nlc/feature-narratives/38-python-call-tree.md |  35 ++
 .../39-language-inventory-scan.md                  |  35 ++
 docs/nlc/feature-narratives/40-python-first.md     |  60 +++
 .../41-typescript-adapter-specimen.md              |  45 ++
 .../42-brownfield-inventory-beta.md                |  45 ++
 .../nlc/feature-narratives/43-durable-workflows.md |  35 ++
 .../44-tag-time-checker-signature.md               |  55 ++
 .../45-zero-parameter-hub-release.md               |  55 ++
 .../feature-narratives/46-github-product-name.md   |  45 ++
 .../47-full-requirement-import.md                  |  55 ++
 docs/nlc/feature-narratives/48-trace-graph.md      |  95 ++++
 .../49-planet-produce-audit-accounting.md          |  65 +++
 docs/nlc/feature-narratives/50-call-envelopes.md   |  55 ++
 docs/nlc/feature-narratives/51-precise-rewrite.md  |  70 +++
 .../52-constraints-as-data-types.md                |  45 ++
 .../53-nothing-changes-except-through-nlc.md       |  60 +++
 .../feature-narratives/54-brownfield-ourselves.md  |  50 ++
 .../55-rules-that-work-together.md                 |  55 ++
 .../56-brownfield-other-repos.md                   |  50 ++
 docs/nlc/feature-narratives/57-other-languages.md  |  60 +++
 .../feature-narratives/58-public-packs-signing.md  |  55 ++
 docs/nlc/feature-narratives/59-low-code-ui.md      |  55 ++
 docs/nlc/flows/01-interview.md                     |  55 ++
 docs/nlc/flows/02-planit.md                        |  80 +++
 docs/nlc/flows/03-emit-pipeline.md                 |  75 +++
 docs/nlc/flows/04-compile-spine.md                 |  85 ++++
 docs/nlc/flows/05-constraint-chain.md              |  65 +++
 docs/nlc/flows/06-install-and-first-app.md         |  75 +++
 docs/nlc/flows/07-verify-and-ship.md               |  65 +++
 docs/nlc/flows/08-hub-charter-change.md            |  55 ++
 docs/nlc/flows/09-hub-release.md                   |  55 ++
 docs/nlc/flows/10-requirement-pack.md              |  65 +++
 docs/nlc/flows/11-delta-regeneration.md            |  65 +++
 docs/nlc/flows/12-brownfield-beta.md               |  45 ++
 docs/nlc/flows/13-rca.md                           |  55 ++
 docs/nlc/flows/14-full-hub-continuity-audit.md     |  55 ++
 docs/nlc/flows/15-full-requirement-import.md       |  55 ++
 docs/nlc/flows/16-trace-graph-run.md               |  75 +++
 docs/nlc/flows/17-planet-run.md                    |  65 +++
 docs/nlc/flows/18-call-envelopes.md                |  65 +++
 docs/nlc/flows/19-precise-rewrite.md               |  70 +++
 docs/nlc/flows/20-constraints-in-running-app.md    |  45 ++
 docs/nlc/flows/21-changes-only-through-nlc.md      |  60 +++
 docs/nlc/flows/22-brownfield-ourselves.md          |  50 ++
 docs/nlc/flows/23-rules-that-work-together.md      |  55 ++
 docs/nlc/flows/24-brownfield-other-repos.md        |  50 ++
 docs/nlc/flows/25-other-languages.md               |  55 ++
 docs/nlc/flows/26-public-packs.md                  |  55 ++
 docs/nlc/flows/27-low-code-ui.md                   |  55 ++
 goals/hub_install/execute.ps1                      |  57 +++
 goals/hub_install/execute.sh                       |  54 ++
 integrity/gate-set-baseline.manifest.sha256        | 118 ++++-
 integrity/hub-content-tree-hash.txt                |   2 +-
 .../assert_install_foreign_skills_passes.py        | 116 ++++-
 .../fitness_install_scope/fitness_install_scope.py |  18 +-
 114 files changed, 7472 insertions(+), 124 deletions(-)
```

