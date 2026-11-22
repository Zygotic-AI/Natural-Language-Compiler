# RCA: release state is spread over many files and checks

**Date:** 2026-11-21 (rewritten 2026-11-22)
**Queue id:** RCA-126-RELEASE-STATE-SPREAD
**Issue:** [#126](https://github.com/Zygotic-AI/Natural-Language-Compiler/issues/126)
**Status:** root confirmed by owner. Kai (Defect Remediator) challenged the first root independently (`/workspace/rca/c1-126-rca-root-challenge-2026-11-22.md`, sha256 `37b0d8c49ed9ac8c493af4361170c716fdfc17e621d84ad193bd502403189782`): it failed the height test. Richard confirmed the corrected root on question card t2423s9053, 2026-11-22, verbatim: "Yes, that's the cause, and put the check in the rewrite." The fix is ADR 0061, the ADR 0025 policy amendment it names, and change branches C2a to C2c.

## 1. Error condition

Releases spend many turns in step 3 (validate). Richard's words on #126: "oh I forget to have you sign this file" "oh, we said we're doing release 8, but I forgot to change a file and it still says 7" "oh, you tagged, but you needed to sign this file first". On #126 he also wrote: "This was all engineered by grokbot and cloud agents." In chat (message t2408u, not #126 text) he wrote: "If it's rules on rules, why not kill all of them and have just the one with the structure I told you earlier?"

## 2. Why-chain

| Rung | Condition | Evidence |
| --- | --- | --- |
| R0 Symptom | Step 3 takes many turns: unsigned files, stale version text, a tag before a signature | #126 body |
| R1 Product | The release apparatus at `f30d618` spreads release state over many files, signatures and gates | 274 files and 8,996 lines deleted by #126; live ruleset `25824126` |
| R2 Growth | Each release defect added or tightened a rule or gate; none was retired | The 19 v0.7.0 RCA packets (S01 to S19, 2026-11-11) each touched a release rule or gate and retired none. Release-named `tools/fitness*` and `tools/assert*` files (counted by file name, so approximate): about 11 at v0.2.0, about 74 at `f30d618` |
| R3 Procedure | The RCA procedure asked each RCA for one more gate in this repo, scoped to one exact error | ADR 0025 decisions 2 and 3 ("until this repository", "This repo is the last stop"); `rules/nlc-0025.json` NLC-0025-02 ("stop only at this repo"); RCA standard: root = "this exact error condition", actionable = "add a check", "Prefer the earliest point where a single gate would have blocked the chain", "the highest-leverage gate" |
| R4 Root | Policy, below | |
| R5 Next upstream | Principles: crew-work-mandate section 1 (a written definition per domain), ADRs 0002, 0003, 0013 | Present and right; not the source (why_not_valid below) |

## 3. Root

How an RCA turns a defect into a change is decided one defect at a time and only ever adds. Nothing requires a fix to be judged against the area's written target or to retire what it replaces, and ADR 0025 capped the climb at this repository. Grokbot and cloud agents followed that policy faithfully, so every release defect became one more rule, gate or signature holding a piece of release state.

- **failed_level:** Policy (Principle > **Policy** > Standard > Rule > Codified constraint). More rules or codified constraints cannot fix it: the policy is what keeps producing them.
- **next_upstream:** the principles in R5.
- **why_not_valid:** the principles already ask for a written target per domain and one repeatable process. What failed is the policy one level down, which turned "learn from each defect" into "add a check per defect". Changing the principles would prevent nothing more.
- **Where the policy is written:** in this repo, ADR 0025 decisions 2 and 3, `rules/nlc-0025.json` NLC-0025-02, and the RCA standard (`.agents/skills/planit/references/root-cause-analysis-standard.md`: the Root and Actionable rows and section 5 items 1 and 3). In the crew process, crew-work-mandate lines 44 and 149 (crockpot `bot-process/`, outside this repo; Kai owns that edit).

## 4. Fix

1. **Policy (the root), in this repo:** ADR 0025 decisions 2 and 3 now say an RCA climbs to the top of the chain within our control (no stop at this repo), names the failed level, judges its fix against the area's written target, lands at or above the failed level, and retires at least what it adds unless the owner signs an exception. NLC-0025-02 and the RCA standard say the same. ADR 0061 names the amendment, so the owner's C1 signature covers it.
2. **Containment (the instance):** ADR 0061, seven steps, one command each; every other release check is deleted (#126 C2b). ADR 0061 is the written target for releases.
3. **The check:** below.

## 5. The check it leaves behind

`tools/validate-rca-packet.py` (the existing validator, no new gate file) refuses a packet with any of:
- no `failed_level`;
- no `domain_definition` pinned by `path` and `sha256`, or one that does not match the file;
- a `fix.level` below `failed_level`;
- a `fix` that lists more `adds` than `retires`, with no `fix.exception` (an owner-signed `.approval.asc` for this RCA record that verifies with `integrity/owner-keys/`).

`fitness-adr-0025-rca-packet` runs it on every `docs/rca/*.packet.json` recorded on or after 2026-11-21, and requires the known-bad specimens to be refused. That fitness runs inside `./nlc gate --profile release`, so a packet that fails makes `./release validate` print `RELEASE_VALIDATE:CODE_DEFECT` and push nothing. Known-bad: KB1 is this RCA's packet as first written (`examples/rca-packet-net-additive/kb1-c1-rev8.json`); KB2 is RCA S07 with its fix stated honestly (adds one check, retires none). Both returned `RCA_PACKET:MET` before the change and are refused after it; this packet is `RCA_PACKET:MET`.

## 6. CTQ that shows the fix worked

- CTQ1: `./release validate` runs per release with no code defect: 1.
- CTQ2: files holding the current version: 1 (`integrity/nlc-version.json`).
- CTQ3: signatures per release: 1.
- CTQ4 (the root): RCA fixes that add more than they retire without an owner exception: 0 (enforced by the check). Release-named checks at each tag do not rise without an owner exception (baseline about 74 at `f30d618`).

## 7. Remediation owners

| # | Level | Owner | Path | Verification |
| --- | --- | --- | --- | --- |
| 1 | Policy | NLC, ratified by the owner's C1 signature | `adrs/0025-belief-no-blame-climb.md` d2-d3, `rules/nlc-0025.json`, the RCA standard | Text diff in C2a to C2c |
| 2 | Codified constraint | NLC | `tools/nouns/validate_rca_packet/`, `tools/nouns/fitness_adr_0025_rca_packet/`, `integrity/schemas/rca-packet.schema.json`, `examples/rca-packet-net-additive/` | KB1 and KB2 refused, this packet MET (#126 plan, Section 10) |
| 3 | Policy (crew) | Kai | crockpot `bot-process/skills/crew-work-mandate/SKILL.md` lines 44 and 149, `conduct-rca-2` section 7 | Outside this repo; not part of #126 |

R3 (named preventive at path level): rows 1 and 2. R4: self-heal yes (each refusal names the field and the fix); future capture yes (the fitness grades every new packet).
