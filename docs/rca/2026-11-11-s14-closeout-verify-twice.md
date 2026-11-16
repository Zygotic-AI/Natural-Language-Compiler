# RCA: closeout proved twice after stale unsigned gate-set manifest

**Date:** 2026-11-11
**Queue id:** RCA-S14
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Do not fold RCA-S18 or RCA-S19 into this record.

---

## 1. Error condition

**Observed.** After committing TODO / FEATURES pin-complete edits, `./nlc verify` failed (`assert-gate-set-manifest-placeholder-sidecar-fails.py` / derived unsigned manifest / content-tree). The producer ran `python3 tools/regen-derived-release-state.py` and `python3 tools/derive-check-inputs.py --write`, then proved again.

**Observed (skill).** [`.agents/skills/release/SKILL.md`](../../.agents/skills/release/SKILL.md) Step 1A item 6: “**Prove once** — `./nlc verify` → `Verify passed.` on the final HEAD. This is the only suite run in closeout. Do not prove before the commit and again after.” Item 3 syncs content-tree stamp only; it does not regen gate-set / derived check inputs after TODO or FEATURES change.

**Not this record.** First-land fitness fail of the install-scope slice (RCA-S18). FEATURES current-ship lag at v0.6.0 (RCA-S19).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | Closeout | Prove → FAIL → remanifest → prove |
| 3 | Step 1A order | Commit TODO/FEATURES then prove, without derived regen |
| 2 | Derived pins | Gate-set / content-tree move when those files move |
| 1 | Skill “prove once” | Assumes the tree is already derived-complete |
| 0 | [ADR 0050](../../adrs/0050-hub-content-tree-hash.md) / mandate | Derived state is part of the commit, not a second prove |

**Furthest controllable point:** closeout “prove once” does not regenerate derived release state after TODO / FEATURES (content-tree / gate-set members) change.

---

## 3. Impact / scope

Closeout ran the suite twice. Unsigned manifest looked like a signature problem. Extra regen commits.

---

## 4. Timeline

| Event | Note |
| --- | --- |
| TODO / FEATURES pin-complete commit | Derived hashes stale |
| `./nlc verify` | FAIL |
| `regen-derived-release-state.py` + `derive-check-inputs.py --write` | Second prove MET |

---

## 5. Mechanism on reproduction

**Confirmed.** Skill Step 1A.6 names a single `./nlc verify`. Step 1A.3 is `sync-hub-content-tree-hash.py` only. TODO and FEATURES are in the content tree; editing them without regen fails the derived unsigned-manifest / stamp binders.

---

## 6. The one thing

Release-skill closeout must regenerate derived release state (`regen-derived-release-state.py` / `derive-check-inputs.py --write` / content-tree stamp) after TODO or FEATURES change, **then** prove once on that HEAD. Prove → remanifest → prove is an incomplete Step 1A, not a second allowed suite.

---

## 7. Prevention test

If regen ran before the only `./nlc verify`, the first prove would have seen current derived files and would not have failed solely on a stale unsigned manifest from those edits.

---

## 8. Contributing factors

- “If FAIL, fix until it passes, then commit that fix and prove once more” in the same bullet encodes the missing regen as a retry instead of a prescribed step.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Insert derived regen (gate-set / check-inputs / content-tree) in Step 1A immediately before the single `./nlc verify`, whenever TODO, FEATURES, or other content-tree members changed. |
| Owner | hub maintainer |
| Path | `.agents/skills/release/SKILL.md` Step 1A |
| Verification | A fixture TODO edit without regen fails a skill-author/closeout check that requires regen-before-prove. Closeout log contains one verify MET. |
| Implementation route | not in this record |

---

## 10. Follow-up

S18/S19 are separate first-land and FEATURES-SSOT defects.
