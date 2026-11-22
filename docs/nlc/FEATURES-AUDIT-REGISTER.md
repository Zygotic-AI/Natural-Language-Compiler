# FEATURES audit register

Working register for [`FEATURES-AUDIT-PLAN.md`](FEATURES-AUDIT-PLAN.md). Product story SSOT remains [`FEATURES.md`](FEATURES.md).

## Gate (default-closed)

| Criterion | Blocking? | Pass when (true if…) | Evidence |
| --------- | --------- | -------------------- | -------- |
| Row coverage | yes | Every FEATURES Released feature has exactly one register row | count match |
| Disposition enum | yes | Status ∈ `UNAUDITED` \| `Correct` \| `Overclaim` \| `Underclaim` | this file |
| Evidence on disposition | yes | Non-`UNAUDITED` rows cite command/path/ADR | Evidence column |
| No silent FEATURES reorder | yes | Order changes only after Stage E acceptance | Acceptance block |

**Done signals.** All Released rows dispositioned; Stage D table complete; Stage E acceptance recorded before FEATURES Upcoming edit; Stage F FEATURES matches acceptance; Stage G tree-fresh MET (verify residual noted).

## Stage G — prove receipt

| Check | Result |
| ----- | ------ |
| Register Gate (coverage / enum / evidence / no silent reorder) | **PASS** |
| FEATURES Upcoming matches Stage E sequence 1–13 | **PASS** |
| hub-content-tree-fresh | **PASS** (RESULT:MET) |
| `./nlc verify` | **FAIL** residual only: `assert-gate-set-manifest-placeholder-sidecar-fails` (out of scope) |
| GATE-STD (plan + register Gate tables) | **PASS** |

## Released rows

| ID | Slice | Feature | Status | Evidence | Notes |
| -- | ----- | ------- | ------ | -------- | ----- |
| R01 | v0.1 | One-line install | Correct | `README.md` curl|bash; `goals/hub_install/execute.sh` exists; `scripts/install.sh` | Front door present; claim: curl on Linux/macOS/WSL; PowerShell on Windows |
| R02 | v0.1 | Checksum-verified install | Correct | `tools/nlc-install-verify.py` + `integrity/nlc-install-hashes.json`; install refuses on fingerprint miss (`INSTALL:NOT_MET hub verify failed`) | Post-install hub fingerprints; not a separate GitHub-asset sha in fetch script; claim: Tagged tarball into a local version store; bad download refu |
| R03 | v0.1 | Compiler lock | Correct | `integrity/schemas/nlc-lock.schema.json`; `tools/nouns/lock_validate/`; local pin `ASSERT:PASS` via `python3 tools/assert-install-local-pin-passes.py` | claim: App repo pinned to one hub version |
| R04 | v0.1 | Greenfield app scaffold | Correct | `./nlc new --help` lists path/name/store; CLI subcommand `new` | claim: `./nlc new` writes `./nlc`, lock, CI verify template |
| R05 | v0.1 | Plain-English interview | Correct | `.agents/skills/interview/SKILL.md`; `python3 tools/assert-interview-packet-fails.py` → `ASSERT:PASS` | claim: `/interview` splits what they said into named goals; no emit |
| R06 | v0.1 | Incremental compile | Correct | `.agents/skills/planit/SKILL.md`; `PLANIT_IDENTITY:MET`; dashboard queues `/planit` | Process skill present; full emit dogfood not re-run this slice; claim: `/planit` compiles one bound goal; small-context code; stop |
| R07 | v0.1 | Tightly scoped emit and refuse | Correct | `docs/nlc/PIPELINE-WIRING.md`; `tools/nlc-pipeline-wire.py`; `python3 tools/assert-emit-audit-fails.py` → `ASSERT:PASS` | First slice; precise rewrite still upcoming per FEATURES; claim: Atomic units; defects at compile time; do not hand-patch gen |
| R08 | v0.1 | Verify path | Correct | `./nlc verify --help` and `./nlc verify-deep --help` exist; ADR 0021 | Full suite currently has unrelated residual gate-set assert; claim: `./nlc verify` and `./nlc verify-deep`; red comes with next |
| R09 | v0.1 | Impact graph | Correct | `docs/spine/IMPACT-GRAPH.md`; `python3 tools/assert-impact-graph-generated.py` → `RESULT:MET` / `ASSERT:PASS` | goal→verb only; not three-query trace graph; claim: Which goals call which noun verbs |
| R10 | v0.1 | Delta regeneration | Correct | `tools/nlc-delta-regen.py --help` (UC9); `--write-queue` supported | claim: Change one requirement; regen queue for the blast radius |
| R11 | v0.1 | Human CLI dashboard | Correct | `./nlc` prints queue + command map; `docs/nlc/MENU.md` | claim: `./nlc` shows the queue and a short command map |
| R12 | v0.2 | Requirement packs | Correct | `./nlc pack {ingest,export,install}`; `docs/nlc/REQUIREMENT-PACKS.md`; `python3 tools/assert-pack-ingest-candidates-passes.py` → ASSERT:PASS; `integrity/uc-product-status.json` packs_v02 closed | claim: Ingest a policy doc into candidates; human approves; export/ |
| R13 | v0.2 | Hub-local pack list | Correct | `docs/nlc/PACK-REGISTRY.md`; `python3 tools/validate-hub-pack-registry.py` → HUB_PACK_REGISTRY:MET; empty packs = install unrestricted | claim: Curated list when it has entries; empty list means install i |
| R14 | v0.2 | Policy to decisions to rules | Correct | ADR→rules path; `./nlc maintainer rule-runner`; `python3 tools/assert-rule-runner-fails.py` ASSERT:PASS; UC4 closed in uc-product-status | Full source→quote import still Upcoming item 1; claim: A standard becomes an accepted decision, then if/then rules |
| R15 | v0.2 | Rule receipts in code | Correct | `./nlc maintainer rule-marker` / `rule-emit`; `python3 tools/assert-rule-marker-emit.py` ASSERT:PASS | claim: Markers on generated code; ask where a tag is enforced |
| R16 | v0.2 | Rules that fight when you accept them | Correct | `python3 tools/assert-rule-adoption-conflicts-fails.py` ASSERT:PASS; `assert-rule-adoption-passes.py` ASSERT:PASS (UC14) | claim: Two accepted rules that are a straight contradiction on the |
| R17 | v0.2 | Knowledge facts before generate | Correct | `./nlc maintainer guide before-generate`; BEFORE_GENERATE:MET/NOT_MET stamp under `.nlc/`; UC18 closed | claim: Facts bound in interview; stamp before generate; refuse stal |
| R18 | v0.2 | Gate after every generate | Correct | `docs/nlc/GATE-RECORD-BINDER.md`; `./nlc maintainer gate-record` / `gate-scope`; `tools/nlc_gate_record.py`; UC21/ADR 0010 | claim: Each artifact gated before the next statement; receipt so ve |
| R19 | v0.2 | Adversarial review | Correct | `.agents/skills/bbp-reviewer/SKILL.md`; `./nlc maintainer plan-audit`; planit Phase 4/6 | claim: Second role attacks the plan before emit |
| R20 | v0.2 | Produce, audit, and ship as separate roles | Correct | `docs/nlc/HUMAN-JUDGMENT-GATES.md` C24 `Released-by:` on CONFIRM.md; distinct bbp-proposer/reviewer/confirmer skills | claim: Human `Released-by:` on `CONFIRM.md` to ship |
| R21 | v0.2 | Change class A–F | Correct | `CHARTER.md` §6 classification A–F; produce package requires class stated (C1) | claim: Ceremony matches risk |
| R22 | v0.2 | Breaking-contract acceptance | Correct | `./nlc maintainer contract-break-accept --help` (ADR 0006) | claim: Break stays red until the requirement is accepted; caller li |
| R23 | v0.2 | Durable workflows with tagged engines | Correct | `python3 tools/assert-durable-engine-rule-fails.py` ASSERT:PASS; `assert-durable-engine-tag-strict-fails.py` ASSERT:PASS (UC13) | claim: Durable goals bind to a named engine; bad pairings fail |
| R24 | v0.2 | Python call-tree inventory | Correct | `./nlc maintainer call-tree --check` → CALL_TREE:MET; UC20 | claim: Verb → interior functions in Python `domain/` |
| R25 | v0.2 | Language inventory scan | Correct | `./nlc maintainer language-scan` exists (UC16 v0); listed languages, not parity | claim: List languages present |
| R26 | v0.2 | Brownfield inventory (beta) | Correct | `./nlc adopt-existing --help`; `./nlc maintainer brownfield-migrate --write-plan/--apply`; FEATURES already labels beta | Still add noun/goal by hand per claim; claim: `./nlc adopt-existing`; plan; v1 apply; still add one noun a |
| R27 | v0.2 | Closed-set expansion | Correct | `./nlc maintainer primitive-propose --name`; UC12 closed in uc-product-status | claim: New primitive or tag is a decision first |
| R28 | v0.2 | Decision log | Correct | `adrs/` current + `adrs/history/` (16 history files); superseded kept | claim: Accepted decisions recorded; old ones superseded, not delete |
| R29 | v0.2 | Defects go upstream | Correct | `python3 tools/assert-upstream-hand-patch-fails.py` ASSERT:PASS (UC10) | claim: Bad emit is an interview/decision/rule miss; hand-patched ge |
| R30 | v0.2 | Emit pipeline gates | Correct | `tools/nlc-pipeline-wire.py`; `docs/nlc/PIPELINE-WIRING.md`; `assert-emit-audit-fails.py` ASSERT:PASS | claim: No emit if the action is not on the plan or decisions are un |
| R31 | v0.2 | Semantic rule apply | Correct | `python3 tools/assert-rule-semantic-apply-fails.py` / `...-passes.py` ASSERT:PASS; pan semantic ASSERT:PASS (UC4/UC5) | claim: Must/forbid on tagged Python goals |
| R32 | v0.2 | Human ship check | Correct | `./nlc ship-check --help` | claim: `./nlc ship-check` |
| R33 | v0.2 | Compiler upgrade | Correct | `./nlc upgrade --help`; ADR 0014 upgrade path | claim: `./nlc upgrade` walks the version chain |
| R34 | v0.2 | Install doctor | Correct | `./nlc doctor` / `doctor fix` help | claim: `./nlc doctor` / `doctor fix` |
| R35 | v0.2 | Retry idempotency checks | Correct | `tools/fitness-c15-idempotent.py`; `python3 tools/assert-c15-fails.py` ASSERT:PASS (known-bad still fails) | Fitness, not dashboard — matches FEATURES note; claim: Fail when a retry would double-apply |
| R36 | v0.2 | Quality as ops vs defects | Correct | `integrity/GATE.md` binary PASS/FAIL; `integrity/QUALITY_METRIC.md`; DESCRIBE ops vs defects | claim: Each gate is pass or fail |
| R37 | v0.2 | RCA packet | Correct | `docs/nlc/RCA-PACKET.md` exists | claim: Record the process miss, not a person |
| R38 | v0.2 | TypeScript adapter specimen | Correct | `examples/non-python-with-adapter/`; `python3 tools/assert-non-python-adapter-fails.py` ASSERT:PASS; teaching/not convert-language | claim: Teaching example only |
| R39 | v0.2 | Adopter CI template | Correct | `templates/adopter/github-workflows-nlc-verify.yml`; `nlc_init.py` copies to `.github/workflows/nlc-verify.yml` | claim: `nlc-init` writes a verify workflow |
| R40 | v0.3-0.7 | Hub release commands with no bump flags | Correct | `./release validate`, `sign`, `main`, `tag` → `scripts/nlc-release.sh` → `tools/nouns/nlc_release_tag_gate/`; the version comes from the branch name; `docs/adoption/RELEASE.md` | claim: Hub maintainers cut a ship with no bump flags |
| R41 | v0.3-0.7 | No editor hooks | Correct | ADR 0058 Status: Accepted; `.cursor/hooks.json` / `.cursor/hooks` absent; FEATURES Released cites verify-on-files | claim: Same compile rules in every harness; `./nlc verify` notices |
| R42 | v0.3-0.7 | Loadable published skills | Correct | `.agents/skills/{interview,planit,verify}/SKILL.md` present; install copies skills via hub_install | claim: `/interview`, `/planit`, `/verify` load after install |
| R43 | v0.3-0.7 | Tag-time checker signature | Correct | ADR 0057; `integrity/checker-digest.sha256` + `.approval.asc` present | claim: Owner signs the checker digest at tag |
| R44 | v0.3-0.7 | GitHub product name | Correct | remote `Zygotic-AI/Natural-Language-Compiler`; README install URLs use that slug | claim: Install from `Zygotic-AI/Natural-Language-Compiler` |
| R45 | v0.3-0.7 | Python-first compiled systems | Correct | `./nlc maintainer call-tree` Python UC20; language-scan inventories only; FEATURES honesty matches Upcoming other-languages | claim: Python apps compile and gate; other languages are listed, no |
| R46 | v0.3-0.7 | Install into a specific repo | Correct | ADR 0060; `python3 tools/assert-install-local-pin-passes.py` ASSERT:PASS; `assert-install-local-dispatch-passes.py` ASSERT:PASS; `fitness-install-scope.py` RESULT:MET; `scripts/nlc-launcher.sh` | claim: Installer asks global or local. Local pins `.nlc/hub` in tha |

## Stage C — Overclaim / Underclaim rollup

| Check | Result |
| ----- | ------ |
| Overclaim count | **0** |
| Underclaim count | **0** |
| FINDINGS.md new rows | **none** — no honesty gaps to open |
| FEATURES wording fixes from audit | **none** required |

Released rows remain **46/46 Correct**. Housekeeping only: Upcoming items 1–2 are already Released (tombstones); Stage F should renumber remaining Upcoming when order is accepted.

## Stage D — remaining order analysis

Scoring rules from [`FEATURES-AUDIT-PLAN.md`](FEATURES-AUDIT-PLAN.md): prefer **high foundation** earlier when deps allow; do not schedule dogfood brownfield before its stated deps; Planet/manifests/envelopes are retrofit-expensive; public packs / UI stay late.

**Already Released (not re-sequenced):** Upcoming §1 no hooks, §2 install-into-repo (and matching Released rows).

| ID | Item | depends_on | unlocks | foundation | dogfood_blocker | Notes |
| -- | ---- | ---------- | ------- | ---------- | --------------- | ----- |
| U3 | Full requirement import | packs ingest (Released); interview | quote→constraint→bind chain; dogfood import | med | **yes** | Current milestone |
| U4 | Trace graph | U3 (richer edges); impact graph (Released) | blast radius for rewrite; audit queries | **high** | **yes** | Ids everything hangs on; retrofit-expensive |
| U5 | Precise rewrite | U4; delta-regen (Released) | architecture swap; no-slop regen | **high** | **yes** | Dirty predicates belong with this |
| U6 | Constraints as data types in running app | U5; U3 onboarding | policy-as-code full job | **high** | **yes** | Running-app enforcement, not compile-only |
| U7 | Brownfield ourselves (dogfood) | U3–U6; install pin; no hooks | real BF learning | med | — | Must not cheat with hub goals |
| U8 | Rules that work together | U7 (real cases) | cross-pack combine | med | no | After dogfood, not before |
| U9 | Brownfield other repos | U7 | customer BF claim | med | no | |
| U10 | Other languages | U7 or U9 as-is readers; Python emit | adoption | med | no | After self-BF |
| U11 | Public packs + signing | U10 (adoption reason); key-rotation design | shared packs | low | no | Stolen-key problem still open |
| U12 | Low-code UI | mature compile path (U3–U6+) | product UI | low | no | Last |
| T-Planet | Planet tenets (manifest + audit both) | emit/gate path (Released); better with U4 ids | auditable produce | **high** | soft | Retrofit-expensive if emit volume grows first |
| T-Acct | Model-call accounting | T-Planet / execution records | cost honesty | **high** | soft | Part of Planet tenet 6 |
| T-RunObs | Run-level observability | T-Planet run-level index | reconstruct runs | **high** | soft | Not per-call bloat |
| T-RCA | RCA same manifest treatment | T-Planet; RCA packet (Released) | failure-path audit | med | soft | |
| T-Producers | Inference producers need manifests | T-Planet | close producer set | med | soft | List already in FEATURES |
| T-Env | Call envelopes | harness-agnostic (Released) | abandon bad calls early | **high** | soft | Pair with file verify |
| T-NLCOnly | Nothing changes except through NLC | T-Env helpful; `/nlc` skill | no back-door edits | med | soft | Verify still catches skips |
| T-Dirty | Dirty predicates on `/release` | U5 | release queue honesty | med | soft | Spec’d under precise rewrite |

### Draft recommended sequence (for Stage E acceptance)

Rationale: keep dogfood spine (import → graph → rewrite → types → self-BF) but **promote Planet + envelopes** immediately after the trace graph so manifests/ids/envelopes are not bolted onto a finished emit surface.

1. **U3** Full requirement import *(milestone — unchanged)*  
2. **U4** Trace graph *(high foundation)*  
3. **T-Planet + T-Acct + T-RunObs + T-RCA + T-Producers** as one “Planet produce/audit accounting” slice *(high foundation; uses graph ids)*  
4. **T-Env** Call envelopes *(high foundation; before more harness surface)*  
5. **U5 + T-Dirty** Precise rewrite + dirty predicates on `/release`  
6. **U6** Constraints as data types in the running app  
7. **T-NLCOnly** Nothing changes except through NLC (`/nlc` routing)  
8. **U7** Brownfield ourselves  
9. **U8** Rules that work together  
10. **U9** Brownfield other repos  
11. **U10** Other languages  
12. **U11** Public packs + signing  
13. **U12** Low-code UI  

**Delta vs today’s FEATURES Upcoming 3–12:** insert Planet bundle + envelopes between graph and precise rewrite; attach dirty predicates to precise rewrite; leave 7–12 relative order intact; drop/renumber tombstone items 1–2.

## Stage E — acceptance

| Field | Value |
| ----- | ----- |
| Accepted | **yes** — 2026-11-14 |
| How | Operator `/planit continue` after Stage D draft sequence was presented (accept draft; no amendments stated) |
| Sequence | Stage D draft 1–13 (import → graph → Planet bundle → envelopes → rewrite+dirty → constraints-as-types → NLC-only → self-BF → combine rules → other BF → languages → public packs → UI) |
| Stage F | Authorized to rewrite FEATURES Upcoming to match this sequence |

**Accepted sequence (canonical):**

1. Full requirement import  
2. Trace graph  
3. Planet produce/audit accounting (tenets + accounting + run-level obs + RCA/producers manifests)  
4. Call envelopes  
5. Precise rewrite + dirty predicates on `/release`  
6. Constraints as data types in the running app  
7. Nothing changes except through NLC (`/nlc` routing)  
8. Brownfield ourselves  
9. Rules that work together  
10. Brownfield other repos  
11. Other languages  
12. Public packs + signing  
13. Low-code UI

## Disposition log

_Append dated notes when slices complete._

### 2026-11-14 — Stage B2 (v0.2.0)

- 28/28 v0.2 rows dispositioned **Correct** with CLI/assert/doc evidence.
- Sample proofs: pack-ingest ASSERT:PASS; HUB_PACK_REGISTRY:MET; rule-adoption-conflict ASSERT:PASS; semantic apply/pan ASSERT:PASS; durable-engine ASSERT:PASS; call-tree CALL_TREE:MET; upstream-hand-patch ASSERT:PASS; assert-c15-fails ASSERT:PASS; non-python-adapter ASSERT:PASS.

### 2026-11-13 — Stage B1 (v0.1.0)

- Seeded register: **46** Released rows (`UNAUDITED` → B1 dispositions for 11 × v0.1).
- Commands: `python3 tools/assert-interview-packet-fails.py` ASSERT:PASS; `python3 tools/assert-impact-graph-generated.py` RESULT:MET; `python3 tools/assert-emit-audit-fails.py` ASSERT:PASS; `python3 tools/assert-install-local-pin-passes.py` ASSERT:PASS; `python3 tools/fitness-install-scope.py` RESULT:MET.
- All eleven v0.1 rows: **Correct** (checksum claim interpreted as post-install hub fingerprint refuse).

### 2026-11-14 — Stage B3 (v0.3.0–v0.7.0)

- 7/7 current-ship rows dispositioned **Correct**.
- Evidence: `./release validate` takes the version from the branch name; hooks absent + ADR 0058; skills present; checker-digest + approval; GitHub slug; Python-first honesty; local install ASSERT:PASS ×2 + RESULT:MET.
- **Released audit complete:** 46/46 Correct; zero Overclaim/Underclaim so far → Stage C may be a no-op FINDINGS rollup.

### 2026-11-14 — Stage C

- Overclaim 0 / Underclaim 0. No FINDINGS.md rows added. No FEATURES wording fixes from Released audit.

### 2026-11-14 — Stage D

- Scored U3–U12 + thinking-list (Planet, envelopes, etc.).
- Draft recommended sequence promotes Planet bundle + call envelopes after trace graph, before precise rewrite.
- Awaiting Stage E acceptance before FEATURES write.

### 2026-11-14 — Stage E

- Accepted Stage D draft 1–13 via operator `/planit continue` (no amendments).

### 2026-11-14 — Stage F

- Wrote FEATURES Upcoming 1–13 to match accepted sequence; tombstoned Released hooks/install out of numbered Upcoming; thinking list emptied (promoted items).
- Milestones: next = import (item 1); medium confidence notes graph then Planet.

### 2026-11-14 — Stage G (prove)

- `python3 tools/sync-hub-content-tree-hash.py` → SYNC:MET; `./nlc gate hub-content-tree-fresh --tree .` → RESULT:MET.
- Adversarial spot-check: 46 register rows Correct; Stage E acceptance before FEATURES write; FEATURES numbered Upcoming = 13 matching accepted sequence; thinking list empty as intended.
- `./nlc verify` → CI:FAIL `assert-gate-set-manifest-placeholder-sidecar-fails` (`ASSERT:FAIL baseline manifest path column != derive_gate_set_paths`) — **pre-existing residual**, out of scope for this plan.
- `./nlc maintainer guide planit-end` → Planit session cleared.

