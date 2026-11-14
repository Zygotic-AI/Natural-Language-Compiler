# FEATURES audit + remaining-order plan

Planit working plan (multi-turn). Not an ADR. Product story SSOT remains [`FEATURES.md`](FEATURES.md). Audit evidence lands in [`FEATURES-AUDIT-REGISTER.md`](FEATURES-AUDIT-REGISTER.md) (created in Stage A). Order changes write back into FEATURES with reasons in the same change ([product-features SSOT](../../.agents/instructions/product-features-ssot.md)).

**Charter class:** C (docs / honesty about what is released).  
**Version class:** Assumption: **patch** (audit + story reorder; no new enforceable law this plan). If Stage E invents a hard rule, stop and open an ADR (becomes minor+).

**Outcome.** (1) Every Released row in FEATURES is either **correct**, **overclaim**, or **underclaim** with cited evidence. (2) Remaining Upcoming + thinking-list items get a **dependency- and foundation-aware** recommended order; FEATURES Upcoming is updated only after that recommendation is accepted.

**Out of scope.** Implementing missing features. Fixing the pre-existing `assert-gate-set-manifest-placeholder-sidecar-fails` residual (tracked separately). Full `ci_fitness` green as a blocker for Stage B row audits when a row’s own proof command passes.

---

## Gate (default-closed)

| Criterion | Blocking? | Pass when (true if…) | Evidence |
| --------- | --------- | -------------------- | -------- |
| Planit identity | yes | `python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md` prints `PLANIT_IDENTITY:MET` | command |
| Plan-audit receipt | yes | `./nlc maintainer plan-audit --from <export.json>` → `plan-audit:MET` while planit active | `.nlc/plan-audit.json` |
| Register exists before claims | yes | `FEATURES-AUDIT-REGISTER.md` exists with one row per Released feature before Stage B marks Correct | path |
| Evidence per Released row | yes | Each register row cites command exit / path / ADR id — not chat memory | register |
| No silent FEATURES reorder | yes | Stage F edits FEATURES only after Stage E acceptance recorded in register | register + diff |
| Law vs story | yes | Overclaims that need law get FINDINGS/ADR follow-up; FEATURES is not used as a fake gate | FINDINGS / ADR list |
| GATE-STD on artifacts | yes | This plan file and the register each keep a Gate table with testable rows | files |

**Done signals.** All Released rows dispositioned; recommended order table complete; FEATURES Upcoming either updated with reasons or explicitly deferred with reason in register.

---

## Resolution (bound)

| Input | Value |
| ----- | ----- |
| Workspace | hub root `Natural-Language-Compiler` |
| Tier | T2 — multi-turn |
| Multi-step | yes — stages A→G; one stage (or one Released slice) per turn preferred |
| Hub | yes |
| planit_skill_path | `.agents/skills/planit/SKILL.md` |

---

## Stages

| # | Stage | Leaf / procedure | Stop predicate | Audit hook |
| - | ----- | ---------------- | -------------- | ---------- |
| A | Seed register from FEATURES Released tables (v0.1 / v0.2 / v0.3–0.7) | inline | Every Released feature name appears once in register with status `UNAUDITED` | Count FEATURES Released rows == register rows |
| B1 | Audit v0.1.0 Released slice | inline + named proof cmds | Each v0.1 row is Correct / Overclaim / Underclaim with evidence | Spot-check: install, lock, verify, impact, delta-regen |
| B2 | Audit v0.2.0 Released slice | inline + UC/fitness proofs | Same for v0.2 rows | Packs, rules, gate-after-generate, ship roles |
| B3 | Audit v0.3.0–v0.7.0 Released slice | inline + ADR 0058/0060 proofs | Same for current-ship rows | release, hooks-absent, local install |
| C | Roll up Released honesty | inline | FINDINGS entries opened for every Overclaim; Underclaims listed for FEATURES wording | FINDINGS diff or explicit none |
| D | Dependency + foundation analysis of remaining | inline | Every Upcoming 3–12 + thinking-list item has deps-in / deps-out / foundation score | Analysis table in register |
| E | Recommend order | inline | Recommended sequence published; **human or explicit “accept Assumption”** recorded before Stage F | register Acceptance block |
| F | Write FEATURES Upcoming (+ renumber) | inline | FEATURES Upcoming matches accepted order; reasons beside items; items 1–2 tombstone/renumber cleaned | FEATURES diff |
| G | Prove | `./nlc verify` (note known residual) + adversarial pass on register | Register Gate PASS; hub-content-tree-fresh MET after edits | commands |

**Turn policy.** Prefer **one of B1 / B2 / B3 / D / E / F per chat turn**. Do not batch all Released audits into one turn unless the operator says so.

---

## Stage B — how to audit a Released row

For each feature:

1. **Claim** — quote FEATURES “What the customer gets” (one line).
2. **Evidence class** — pick at least one: fitness/assert command, `./nlc` surface, ADR Accepted + in-tree enforcement, documented known-bad.
3. **Run or cite** — full command + exit code, or path to ADR + gate that enforces it.
4. **Disposition**
   - **Correct** — evidence matches the claim at the honesty level FEATURES states (including “first slice” / “beta”).
   - **Overclaim** — marketing or absolute wording exceeds what the tree enforces.
   - **Underclaim** — tree clearly ships more than FEATURES admits (optional FEATURES expand).
5. **Follow-up** — Overclaim → FINDINGS row or FEATURES wording fix in Stage C/F; do not “fix” by deleting the product.

Pre-existing verify residual (`assert-gate-set-manifest-placeholder-sidecar-fails`) does **not** auto-fail every row. A row fails only when **its** named evidence fails or is missing.

---

## Stage D — how to score remaining work

For each remaining item (Upcoming 3–12 that are not already Released, plus thinking-list):

| Field | Meaning |
| ----- | ------- |
| `depends_on` | Features / ADRs that must exist first |
| `unlocks` | What becomes cheaper or possible after this |
| `foundation` | `high` / `med` / `low` — high = expensive to retrofit later (data model, graph identity, emit contracts, Planet manifest shape, call envelopes) |
| `dogfood_blocker` | Blocks “brownfield ourselves” or honest self-import if missing |

**Ordering rules (normative for the recommendation):**

1. Prefer **high foundation** earlier when dependencies allow.
2. Do not schedule dogfood brownfield before its stated deps (import, graph, precise rewrite, constraints-as-types, install pin, no hooks — per FEATURES today).
3. Planet / manifests / envelopes are foundational accounting — if they must eventually wrap all inference producers, prefer them **before** large new emit surfaces, unless they hard-depend on the trace graph ids.
4. Public packs / UI stay late (network + product surface).
5. Reorder only with written **why** next to the item when Stage F runs.

---

## Product statements (one boundary each)

1. **Register** — Create and fill `FEATURES-AUDIT-REGISTER.md` until every Released feature has a disposition.
2. **Honesty** — Open FINDINGS (or FEATURES wording fixes) for Overclaims; do not leave known overclaims unmarked.
3. **Order** — Produce and accept a recommended remaining-order table; then update FEATURES Upcoming in one change with reasons.

---

## Bindings

| Statement | Bound to |
| --------- | -------- |
| FEATURES is story SSOT | `.agents/instructions/product-features-ssot.md`, `AGENTS.md` |
| Law stays in ADRs | `CHARTER.md`, `adrs/` |
| UC machine status companion | `integrity/uc-product-status.json`, `docs/USE-CASES.md`, `TODO` |
| BBP always on | `CHARTER.md` |
| Planit multi-turn | `.agents/skills/planit/SKILL.md`, `docs/nlc/compiler/PLANIT-ORCHESTRATION.md` |

---

## Next turn

**Done:** A→G complete. Released 46/46 Correct; FEATURES Upcoming 1–13 matches Stage E; tree-fresh MET; verify residual (`assert-gate-set-manifest-placeholder-sidecar-fails`) noted out of scope.

Plan closed unless the operator opens a follow-up (gate-set residual, presentations stack, etc.).
