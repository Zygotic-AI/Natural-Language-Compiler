# RCA: FEATURES current ship said v0.5.0 while tag was v0.6.0

**Date:** 2026-11-11
**Queue id:** RCA-S19
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Do not fold RCA-S14 into this record.

---

## 1. Error condition

**Observed.** At git tag `v0.6.0` (`28ac221c8618ac7ae2862f059ed8c30b4b3044e0`), [`docs/nlc/FEATURES.md`](../../docs/nlc/FEATURES.md) still said current ship **v0.5.0**:

```text
| [Released](#released) | In the current ship (today **v0.5.0**) |
Current ship: **v0.5.0**.
### v0.3.0–v0.5.0 (current ship)
```

`integrity/nlc-version.json` and the tag name were **v0.6.0**. The prose was aligned to v0.7.0 only during v0.7.0 closeout (pin-a-repo TODO done). At tag `v0.7.0` the same file says **v0.7.0**.

**Observed (gates).** F1 [`fitness-findings-shipped-tag-sync.py`](../../tools/fitness-findings-shipped-tag-sync.py) grades FINDINGS and DESCRIBE only. `git grep FEATURES tools/ -- glob '*.py'` has no fitness binder on FEATURES current-ship. [`.agents/instructions/product-features-ssot.md`](../../.agents/instructions/product-features-ssot.md) is chat-only.

**Not this record.** Closeout prove-twice (RCA-S14).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | FEATURES.md at `v0.6.0` | Current ship v0.5.0 |
| 3 | Release-prep / WRITE_RECORD | Updates FINDINGS/DESCRIBE/record, not FEATURES |
| 2 | F1 | No FEATURES path |
| 1 | product-features-ssot instruction | No machine refuse |
| 0 | [ADR 0050](../../adrs/0050-hub-content-tree-hash.md) content tree | FEATURES is in the tree; identity sync does not read it |

**Furthest controllable point:** shipped identity (tag + version file) can disagree with FEATURES “current ship” because no binder grades that sentence.

---

## 3. Impact / scope

Product SSOT told adopters the current ship was v0.5.0 for the entire v0.6.0 tag lifetime. Aligned only as a side effect of a later closeout.

---

## 4. Timeline

| Event | Note |
| --- | --- |
| Tag `v0.6.0` | FEATURES current ship v0.5.0 |
| v0.7.0 closeout | FEATURES current ship moved to v0.7.0 (skipped stating v0.6.0 as current) |
| Tag `v0.7.0` | FEATURES current ship v0.7.0 |

---

## 5. Mechanism on reproduction

**Confirmed.** `git grep -n "current ship" v0.6.0 -- docs/nlc/FEATURES.md` shows v0.5.0. F1 source list: `FINDINGS.md`, `DESCRIBE.md` only. Instruction file has no fitness partner.

---

## 6. The one thing

Release-prep / F1 (or a dedicated binder) must require `docs/nlc/FEATURES.md` current-ship text to match the version being tagged (`integrity/nlc-version.json` / planned tag). Chat instruction without a binder cannot prevent a lagging header.

---

## 7. Prevention test

If that binder had been in place, `v0.6.0` could not have been tagged while FEATURES said v0.5.0. VERIFY_TARGET / tag gate would have refused.

---

## 8. Contributing factors

- Prep surfaces tool does not touch FEATURES.
- S14 later remanifested FEATURES edits; that is derived-hash, not this identity lag.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Extend F1 or add a fitness that parses FEATURES current-ship and requires equality with `integrity/nlc-version.json` (and the tag at tag-time). Include FEATURES in PREP surfaces. |
| Owner | hub maintainer |
| Path | `tools/nouns/fitness_findings_shipped_tag_sync/`; `tools/nlc_release_prep_surfaces.py`; `.agents/instructions/product-features-ssot.md` remains prose |
| Verification | A fixture FEATURES “today v0.5.0” with version 0.6.0 prints NOT_MET. Tag-time `v0.6.0` with that fixture cannot MET. |
| Implementation route | not in this record |

---

## 10. Follow-up

Do not treat a closeout edit of FEATURES as prevention of the next lag.
