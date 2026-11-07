# Contributors

Contributions that meet the standards in [CONTRIBUTING.md](CONTRIBUTING.md) will be considered. We prefer contributors who take long-term ownership of a specific area rather than one-off patches.

Areas are listed in order of expected impact for the current phase (Python-first hub, pre-v1 compliance packs and multi-language parity). Primary owner is listed first.

| Area | Status | Owner / Primary | Additional contributors | Notes |
|------|--------|-----------------|-------------------------|-------|
| **Process / Systems Engineering** | Closed | [richardpickett](https://github.com/richardpickett) | — | Lean Six Sigma, RCA, audited work loops, change-class design, produce≠audit≠ship. Core of the charter and PLANIT orchestration. |
| **Metaprompt / Agent Skill Authoring** | Open for long-term ownership | — | AI-assisted alongside process work | `.agents/skills/` (interview, planit, verify, full-nlc-audit, bbp-*, requirement-pack-ingest), failure-mode catalogs, domain-first authoring. |
| **Python Gate & Tooling** | Covered under Process/Systems + AI | [richardpickett](https://github.com/richardpickett) (via process work) | Open for dedicated long-term owner | `tools/` fitness checks, scanners, impact graph, delta-regen, rule runners, CI fitness. Day-to-day mechanical spine. |
| **Technical Writing & Documentation Stewardship** | Open for long-term ownership | — | — | TERMS, GLOSSARY, CHARTER, MANIFESTO, JOBS-TO-BE-DONE, adoption guides. Consistency prevents drift. |
| **CLI / Packaging / Cross-Platform** | Covered under Process/Systems + AI | [richardpickett](https://github.com/richardpickett) (via process work) | — | Installers, `nlc` doctor/menu, lock files, release tooling, Windows/macOS/Linux parity. |
| **Human Factors / Interview Design** | Open for long-term ownership | — | — | `/interview` skill, interview-packet validation, goal/requirement ratification flows for non-process-engineers. |
| **Security & Auditability Engineering** | Open for long-term ownership | — | — | Traceability, gate receipts, process supervision, blast-radius analysis, human-signature paths. |
| **Benchmark & Evaluation** | Open for long-term ownership | — | — | Formal eval design, adversarial testing, compile-or-refuse metrics, findings/use-case coverage. |
| **Vertical Example / Dogfood Building** | Open for long-term ownership | — | — | Greenfield/brownfield examples that surface real gaps and feed FINDINGS. |
| **Compliance & Regulatory Domain Expertise** | Post-v1 | — | — | HIPAA, GDPR, PCI-DSS, FedRAMP, SEC, etc. Requirement packs and bindable rules. Not in scope until after v1. |
| **Multi-Language Adapter Development** | Post-v1 | — | — | Scanners and gates for TypeScript, Go, Rust, etc. (UC16/UC20 expansions). Python-first today. |

Long-term ownership means sustained responsibility for the area’s standards, gaps, and evolution—not a single PR. Open areas are open to interview for that ownership.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution bar and process.
