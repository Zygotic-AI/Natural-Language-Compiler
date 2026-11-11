# RCA: first land of install-scope failed hub fitness / CI

**Date:** 2026-11-11
**Queue id:** RCA-S18
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Do not fold RCA-S14 into this record.

---

## 1. Error condition

**Observed.** The ADR 0060 (install global vs local pin) slice was offered before hub fitness was MET on that HEAD.

**Observed (GitHub, PR #68).** First fitness on `cursor/install-foreign-skills-check-326d` SHA `31900d78`:

- push run `42882750057` failure (2026-11-10T19:11:24Z)
- pull_request run `42882799213` failure (2026-11-10T19:11:42Z)

Log excerpt: `FAILED hub-content-tree-fresh`; `VIOLATION hub-content-tree-hash … != content digest`; `CI:FAIL tools/assert-gate-set-manifest-placeholder-sidecar-fails.py`; `FULL_NLC_AUDIT:NOT_MET`. Follow-up commit `2c179d0b` (“include new install landmine in the gate-set snapshot”) then passed.

**Observed (PR #69).** Merged 2026-11-10T22:27:24Z. Listed GitHub runs on that branch succeeded; the tree still contains follow-up regen commits `08d9021c` (“refresh derived release state after install-scope”) and `41d5e6c` (“regenerate unsigned gate-set manifest after pin closeout”) — the same derived-state class as the #68 fail.

**Prior RCA.** [`2026-11-02-pr-offered-before-fitness-success.md`](2026-11-02-pr-offered-before-fitness-success.md): offer before verify/fitness MET. Recurrence on a feature slice, not only `/release`.

**Not this record.** Closeout prove-twice after TODO/FEATURES (RCA-S14).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | CI | First HEAD failed verify |
| 3 | `gh pr create` / offer | PR existed before MET |
| 2 | Feature produce path | Did not run `pr-offer-gate.py` / `./nlc verify` as a refuse before create |
| 1 | 2026-11-02 RCA | Named this for release skill; feature slices still offer red HEADs |
| 0 | Skill 5b | “Only pr-offer-gate may `gh pr create`” is not bound on non-ship PRs |

**Furthest controllable point:** a feature pull request can be created without `./nlc verify` MET and without `pr-offer-gate.py` on that HEAD.

---

## 3. Impact / scope

Red CI on first land. Extra commits to stamp / gate-set / landmines. Same class as 2026-11-02.

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-11-10T19:11:24Z | #68 first push fitness FAIL `31900d78` |
| 2026-11-10T19:11:42Z | #68 first pull_request fitness FAIL |
| 2026-11-10T19:18:52Z | `2c179d0b` landmine/gate-set fix; later runs success |
| 2026-11-10T22:27:24Z | #69 merged (after derived regen commits) |

---

## 5. Mechanism on reproduction

**Confirmed.** Failed run `42882799213` log lines above. Follow-up commit message names the missing landmine in the gate-set snapshot. `pr-offer-gate.py` is the release-skill offer path; nothing in the feature produce path exits non-zero in front of `gh pr create` when verify would fail.

---

## 6. The one thing

Every hub pull-request create (feature slice included) must run `python3 tools/pr-offer-gate.py` (or an equivalent that refuses unless `./nlc verify` is MET on that HEAD). Direct `gh pr create` of a failing tree is not an offer step. The 2026-11-02 refuse applies beyond `/release`.

---

## 7. Prevention test

If that refuse had been in place, `31900d78` could not have opened as #68 while `hub-content-tree-fresh` and the unsigned manifest failed. The first-land red CI could not have occurred.

---

## 8. Contributing factors

- New landmines not in the gate-set snapshot (output defect; process is offer-before-prove).
- S14 is closeout regen after TODO/FEATURES, a later instance of missing derived regen.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Bind `pr-offer-gate.py` (verify MET before `gh pr create`) on all hub PR creates, not only the ship skill. Feature slices must prove once on the offered HEAD. |
| Owner | hub maintainer |
| Path | `.agents/skills/release/SKILL.md` is not enough; portable produce/offer instruction or a git/CI refuse on unverified creates |
| Verification | A fixture tree that fails `./nlc verify` cannot print `PR_OFFER_GATE:MET`. First GitHub fitness on a new feature PR is not a first-seen fail of stamp/manifest. |
| Implementation route | not in this record |

---

## 10. Follow-up

Cite 2026-11-02. S14 remains the later closeout prove-twice.
