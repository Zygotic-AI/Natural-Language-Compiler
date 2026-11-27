# ADR enforcement

Every **Accepted** [ADR](../adrs/README.md) must map to **runnable** binders (tools, `./nlc verify` blockers, CI landmines, or prescribed skills)—not prose alone.

**Status SSOT:** checklist in repo [`TODO`](../TODO) (ADR enforcement section). This file holds the per-ADR table; **bound** means hub compile CI proves the binder set (meta-fitness + landmines), not that every adopter runtime path is complete.

| ADR | Must be enforced by (target) | Status |
| --- | --- | --- |
| 0001 | `fitness-adr-0001-binder.py` + `assert-binding-matrix-met.py` | bound |
| 0002 | `fitness-p2-hub-scope.py` + `assert-p2-hub-scope-passes.py` | bound |
| 0003 | `fitness-agent-noun-structure` + landmines | bound |
| 0004 | `fitness-adr-0004-0005-binder.py` + produce/verify-deep landmines | bound |
| 0005 | (with 0004) SSOT + `fitness-produce-ssot-binder.py` + quality fixtures | bound |
| 0006 | contract_change on non-specimen adopters + diff-scoped C10/C21 + `fitness-verify-pipeline-wired` + landmines | bound |
| 0007 | `nlc_rule_runner.py --check` + `assert-rule-semantic-pan-fails.py` + `assert-rule-semantic-apply-fails.py` | bound |
| 0008 | `fitness-adr-0008-binder.py` + specimen + invoice-correct MET landmine | bound |
| 0009 | `nlc_call_tree.py --check` + `assert-verb-primitive-inventory-fails.py` | bound |
| 0010 | `fitness-adr-0010-binder.py` + gate landmines | bound |
| 0011 | `fitness-nlc-naming.py` + landmine | bound |
| 0012 | `check-rule-adoption.py` + conflict landmine + `assert-rule-adoption-tier-diff-fails.py` | bound |
| 0013 | `hub_tool` fitness + landmine | bound |
| 0014 | migration + `assert-migration-step-noop-passes.py` | bound |
| 0015 | `fitness-distribution-binder.py` + install landmines | bound |
| 0016 | `fitness-hub-no-product-requirements.py` + landmine | bound |
| 0017–0018 | `fitness-human-surface-binder.py` + interview landmines | bound |
| 0019 | `fitness-guide-orchestration.py` + `fitness-lifecycle-state-headers.py` + landmine | bound |
| 0020 | (with 0017–0018) MENU/HARNESS + dashboard fitness | bound |
| 0021 | `nlc verify` / `verify-deep` | bound |
| 0023 | `rule_coverage_blockers` + `nlc_rule_emit.py` + binder fitness + landmines | bound |
| 0024 | `fitness-adr-0024-binder.py` + `nlc-action-plan-gate.py` + `nlc-reverse-audit.py` + `nlc-emit-manifest-enforce.py` (ADR 0026) | bound |
| 0025 | `rules/nlc-0025.json` + `validate-rca-packet.py` + `fitness-adr-0025-rca-packet.py` + landmine | bound |
| 0026 | `nlc-action-plan-gate.py` + `nlc-reverse-audit.py` + `nlc-emit-manifest-enforce.py` + specimens + fitness wrappers | bound |
| 0027 | `nlc-emit-from-prose.py` + `fitness-nlc-emit-from-prose.py` | bound |
| 0028 | `fitness-verb-set-lineage.py` + `assert-verb-set-extension-fails.py` | bound |
| 0029 | lineage-check + bind-snapshot + freshness + fitness | bound (v1) |
| 0030 | `nlc-pipeline-wire.py` + `nlc-action-gates.py` + `nlc_emit_audit.py` + `fitness-nlc-pipeline-wire.py` | bound |
| 0031–0035 | `integrity/charter-ratify-backlog.json` + `fitness-adr-record-gate.py` | bound (v1) |
| 0036 | `fitness-nlc-0036-inference-only.py` + `rules/nlc-0036.json` (goals, requirements, knowledge domains) | bound |
| 0037 | `integrity/charter-ratify-backlog.json` non_r_residuals + ADR text | bound (docs/backlog) |
| 0038 | `fitness-adr-0038-no-memory.py` + `rules/nlc-0038.json` | bound (v1) |
| 0039 | `nlc_release_tag_gate` noun + `assert-tag-digest-signature-required-fails.py` (ADR 0061) | bound |
| 0040 | `nlc_release_tag_gate` noun + `assert-tag-digest-signature-required-fails.py` (ADR 0061) | bound |
| 0041 | `product-completion-scope.json` + `hub-pack-registry.json` + `fitness-product-completion-scope.py` + `fitness-hub-pack-registry.py` | bound (v1) |
| 0042 | `rule-ir-product-boundary.json` + `fitness-adr-0007-product-boundary.py` + rule-runner landmines | bound (v1) |
| 0043 | `uc14-product-boundary.json` + `fitness-uc14-product-boundary.py` + rule-adoption landmines | bound (v1) |
| 0044 | `nlc_release_tag_gate` noun + `assert-tag-digest-signature-required-fails.py` (ADR 0061) | bound |
| 0046 | `fitness-planit-identity.py` + `assert-planit-other-skill-fails.py` | bound |
| 0047 | `fitness-adr-approval.py` + `assert-adr-approval-mismatch-fails.py` | bound |
| 0048 | `fitness-executable-shape.py` + `assert-executable-kernel-exempt-fails.py` | bound |
| 0050 | `fitness-no-history-ids-in-evidence.py` (inside `./release validate`) | bound |
| 0051 | `fitness-hub-scope-derived.py` + `assert-produce-handoff-refused.py` | bound |
| 0052 | `fitness-adr-owner-sidecar.py` + `assert-unsigned-codified-does-not-bind-fails.py` | bound |
| 0054 | `fitness-skill-author-check-presence.py` + `fitness-skill-author-checklist.py` + `fitness-skill-content-type.py` + `assert-skill-author-check-fails.py` | bound |
| 0055 | `fitness-live-self-ref-activation.py` + `assert-live-self-ref-direct-edit-fails.py` | bound |
| 0057 | `fitness-derived-release-state.py` + `assert-tag-digest-signature-required-fails.py` | bound |
| 0058 | `fitness-goal-write-hook.py` + `assert-goal-write-hook-landmine-passes.py` | bound |
| 0059 | `fitness-adr-history.py` + `assert-adr-history-fails.py` | bound |
| 0060 | `fitness-install-scope.py` + `assert-install-local-dispatch-passes.py` + local-pin / outside-repo landmines | bound |
| 0061 | `fitness-release-readiness.py` + `assert-open-milestone-issue-fails.py` | bound |
| 0062 | `fitness-constraint-stack.py` + `assert-unsigned-codified-does-not-bind-fails.py` | bound |
| 0063 | `fitness-adr-decision-point-register.py` | bound |
| 0064 | `fitness-lifecycle-state-headers.py` + `assert-work-queue-json-not-ssot-fails.py` | bound |
| 0065 | `fitness-type-dependency.py` + `assert-state-walk-child-drop-fails.py` | bound |

**0007/0009:** semantic rule application and the verb-to-primitive inventory are bound. The pan-return landmine and the inventory mismatch landmine are the failing fixtures. ADR 0023 marker emit stays bound via `rule-emit` / `goal-scaffold` / verify audit.

**Specimens:** `product_tree.is_specimen` skips `CONFIRM` requirements and **ADR 0006** `contract_change_blockers` unless the README includes `contract-change applies` (see `product_tree.contract_change_applies`).

Update this table when hub binder coverage changes.
