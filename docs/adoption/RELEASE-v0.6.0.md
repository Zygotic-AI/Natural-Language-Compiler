# Natural Language Compiler hub v0.6.0

## Highlights

Hub **v0.6.0** is a minor on **v0.5.0**.

- **Product story file.** [`docs/nlc/FEATURES.md`](../nlc/FEATURES.md) is the single place for what is released, what is upcoming, which slices sit on a milestone, and why that order — so operators can argue from the file instead of rehashing chat.
- **Harness- and model-agnostic (ADR 0058).** NLC does not ship or rely on editor/harness hooks. In-tree Cursor hooks are removed; compile correctness stays on `./nlc verify` / verify-deep and the stamps those commands already check.
- **One tag-time owner signature (ADR 0057).** The owner signs `integrity/checker-digest.sha256` for the tag. Branch verify does not require that armor or per-ADR detached signatures as a merge gate.
- **ADR history and separate records.** ADR revision/history folder (ADR 0059); executable-shape and release-planner ADRs accepted as separate records (0048/0049). ADR 0046 (repository Planit identity) is rejected.
- **Contributors map.** [`CONTRIBUTORS.md`](../../CONTRIBUTORS.md) lists ownership areas with GitHub portraits. CG-R4 still refuses person-as-actor prose in process/decision SSOT; attribution on that page is allowed.

## Changes since v0.5.0

- Narrow CG-R4 to person-as-actor prose and allow CONTRIBUTORS portraits. (`6ad1afe`)
- Ratify the v0.6.0 checker digest and drop person names from CONTRIBUTORS. (`4ae4fd1`)
- Remove Cursor harness hooks after ADR 0058 (`e847dfc`)
- Accept ADR 0058 (harness- and model-agnostic) (`b955d18`)
- Accept ADR 0057: tag-time checker digest (`edd686c`)
- Accept ADR 0056: per-file detached owner signatures (`a4dd54d`)
- Accept ADR 0059: revision and history folder (`33a92cc`)
- Accept ADRs 0048 and 0049 as separate records (`eb46c17`)
- Redraft proposed ADRs 0048 and 0049 as separate records (`412c254`)
- Link CONTRIBUTORS.md from README Participate section (`4281dd4`)
- Link CONTRIBUTORS.md from CONTRIBUTING.md (`0e65d1e`)
- Add CONTRIBUTORS.md with ownership areas ordered by impact (`5fc55fb`)
- Reject ADR 0046 repository Planit identity (`b3ccb41`)
- Record compile-chain words and unsequenced upcoming features (`31fbdc8`)
- Rename ADR 0058 to harness- and model-agnostic (`506ba14`)
- Add the product features story file and propose no harness hooks (`126a822`)

### Diff stat

```
.agents/instructions/product-features-ssot.md      |  23 ++
 .agents/skills/planit/SKILL.md                     |   2 +-
 .cursor/hooks.json                                 |  18 --
 .cursor/hooks/nlc-goal-write-gate.sh               | 122 --------
 .cursor/hooks/nlc-planit-identity.sh               |  10 -
 .cursor/hooks/nlc-session-remind.sh                |   9 -
 .cursor/rules/product-features-ssot.mdc            |  10 +
 .nlc/hooks.example.json                            |   5 +-
 .nlc/work-queue.json                               |   8 -
 AGENTS.md                                          |   5 +-
 CONTRIBUTING.md                                    |   2 +
 CONTRIBUTORS.md                                    |  23 ++
 DESCRIBE.md                                        |   1 +
 FINDINGS.md                                        |   3 +-
 README.md                                          |   3 +-
 TODO                                               |  34 ++-
 ...losed-atomic-verb-set-and-policy-adr-lineage.md |  20 +-
 ...029-adr-lineage-active-set-and-bind-snapshot.md |  23 +-
 adrs/0048-executable-shape.md                      |  45 ++-
 adrs/0049-release-planner-owns-stops.md            |  46 ++-
 adrs/0051-hub-own-produce-principles.md            |  25 +-
 .../0052-owner-openpgp-ratification-amends-0051.md |  21 +-
 adrs/0055-staged-activation-of-gate-machinery.md   |   3 +-
 adrs/0056-per-file-adr-detached-signatures.md      |  10 +-
 adrs/0057-tag-time-checker-digest.md               |   6 +-
 adrs/0058-harness-and-model-agnostic.md            |  52 ++++
 adrs/0059-adr-revision-and-history.md              |  58 ++++
 adrs/ACTIVE.md                                     |   6 +
 adrs/CATALOG.md                                    |  14 +-
 adrs/INDEX.md                                      |  22 +-
 adrs/README.md                                     |  22 +-
 ...sed-atomic-verb-set-and-policy-adr-lineage-1.md |  66 +++++
 ...tomic-verb-set-and-policy-adr-lineage-1.md.asc} |   0
 ...9-adr-lineage-active-set-and-bind-snapshot-1.md |  71 +++++
 ...-lineage-active-set-and-bind-snapshot-1.md.asc} |   0
 .../0046-repository-planit-identity-1.md}          |  10 +-
 .../0046-repository-planit-identity-1.md.asc}      |   0
 .../0047-adr-approval-receipts-1.md}               |   0
 .../0047-adr-approval-receipts-1.md.asc}           |   0
 adrs/history/0051-hub-own-produce-principles-1.md  | 128 +++++++++
 .../0051-hub-own-produce-principles-1.md.asc}      |   0
 ...052-owner-openpgp-ratification-amends-0051-1.md |  76 +++++
 ...wner-openpgp-ratification-amends-0051-1.md.asc} |   0
 .../0053-0051-0052-text-retrofit-1.md}             |  10 +-
 .../0053-0051-0052-text-retrofit-1.md.asc}         |   0
 .../0055-staged-activation-of-gate-machinery-1.md  |  80 ++++++
 ...5-staged-activation-of-gate-machinery-1.md.asc} |   0
 content-types/HOW-TO-ADD.md                        |   8 +-
 docs/ADR-ENFORCEMENT.md                            |   4 +
 docs/JOBS-TO-BE-DONE.md                            |   2 +-
 docs/TERMS.md                                      |  28 +-
 docs/USE-CASES.md                                  |   2 +-
 docs/bba/POLICY-ADR-LINEAGE.md                     |   9 +-
 docs/nlc/FEATURES.md                               | 312 +++++++++++++++++++++
 docs/nlc/HARNESS.md                                |   2 +-
 .../IMPLEMENTATION-COMPLEXITY-EXAMINATION-PLAN.md  |   2 +-
 docs/nlc/README.md                                 |   4 +
 docs/nlc/compiler/GLOSSARY.md                      |   4 +
 docs/nlc/effective-decisions.md                    |   2 +-
 integrity/CONTRIBUTION.md                          |  20 +-
 integrity/HUB-IN-FORCE-EXCLUSIONS.md               |  13 +-
 integrity/LEXICON.md                               |   4 +-
 integrity/adr-0051-0052-rules.json                 | 157 ++++-------
 integrity/adr-gates.json                           |  56 ++--
 integrity/audits/A-R22.md                          |   2 +-
 integrity/check-inputs.json                        |  29 +-
 integrity/checker-digest.sha256                    |   2 +-
 integrity/checker-digest.sha256.approval.asc       |  14 +-
 integrity/gate-set-baseline.manifest.sha256        | 168 ++++++-----
 integrity/hub-content-tree-hash.txt                |   2 +-
 integrity/known-bad-cases.json                     |  24 +-
 integrity/mandated-paths.json                      | 168 +++++++----
 integrity/nlc-install-hashes.json                  |   2 +-
 integrity/planit-skill-registry.json               |   2 +-
 integrity/releasable-gates.json                    |   3 +-
 integrity/self-ref-set.json                        |   5 -
 templates/adopter/hooks.example.json               |   5 +-
 tools/assert-adr-history-fails.py                  |  13 +
 tools/fitness-adr-history.py                       |  13 +
 tools/nouns/adr_history/README.md                  |   3 +
 tools/nouns/adr_history/__init__.py                |   1 +
 tools/nouns/adr_history/adjectives.txt             |   1 +
 tools/nouns/adr_history/adr_history.py             |  86 ++++++
 tools/nouns/adr_history/fields.txt                 |   0
 tools/nouns/adr_history/schemas/verbs.schema.json  |  10 +
 tools/nouns/adr_record_gate/adr_record_gate.py     |   2 +-
 tools/nouns/assert_adr_history_fails/README.md     |   3 +
 tools/nouns/assert_adr_history_fails/__init__.py   |   1 +
 .../nouns/assert_adr_history_fails/adjectives.txt  |   1 +
 .../assert_adr_history_fails.py                    |  63 +++++
 tools/nouns/assert_adr_history_fails/fields.txt    |   0
 .../schemas/verbs.schema.json                      |  10 +
 .../assert_goal_write_hook_landmine/README.md      |   3 +
 .../assert_goal_write_hook_landmine.py             | 199 +++----------
 .../assert_hub_in_force_exclusions.py              |   1 +
 .../assert_verifier_change_via_staging_passes.py   |  12 -
 tools/nouns/ci_fitness/ci_fitness.py               |   4 +
 .../fitness_adr_0051_0052_rules.py                 |   2 +-
 .../fitness_adr_superseded.py                      |  15 +-
 tools/nouns/fitness_goal_write_hook/README.md      |   4 +-
 .../fitness_goal_write_hook.py                     |  81 ++++--
 .../fitness_hub_public_self_contained/README.md    |   2 +-
 .../fitness_hub_public_self_contained.py           |   7 +-
 .../hub_in_force_surfaces/hub_in_force_surfaces.py |  10 +
 104 files changed, 1885 insertions(+), 809 deletions(-)
```

