# RCA: AWAIT publication, then silence until poked

**Date:** 2026-11-11
**Queue id:** RCA-S06
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only.

---

## 1. Error condition

**Observed.** `./release` reached `RELEASE:AWAIT publication` (`goals/hub_release/execute.sh` AWAIT kind, action not `EXIT_AWAIT`: prints `RELEASE:AWAIT publication for ${tag}; resume with ./release` and exits 0).

**Observed (GitHub).** Release `v0.7.0` published 2026-11-10T23:50:53Z (`gh release view v0.7.0`). The producer session did not resume `./release` to print `RELEASE:MET v0.7.0 shipped` until the human manager asked “how’s it going?” about 2026-11-11T01:18Z (~90 minutes later).

**Observed (wake).** A `cursor-subscriptions` watch on `github:ci:branch` for branch `v0.7.0` does not fire on GitHub Release publication. Tag `v0.7.0` is not that branch.

**Not this record.** Tag creation. Extra merges (S03–S05).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | Chat silence | No `RELEASE:MET` until poked |
| 3 | Executor AWAIT | Exits 0 and tells the session to resume; does not poll |
| 2 | Release skill done-signals | Lists “awaiting the release pull-request merge, complete”; no publication wake |
| 1 | Subscription kind | CI on branch `v0.7.0`, not Release / tag |
| 0 | [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) `OBSERVE_PUBLISH` | AWAIT is a planner stop that expects a resume, not an unattended wait |

**Furthest controllable point:** after `RELEASE:AWAIT publication`, nothing in the skill or orchestrator binds a wake (GitHub Release event or timer) that re-invokes `./release`.

---

## 3. Impact / scope

The GitHub Release existed while the session looked stalled. The human manager had to poke. `RELEASE:MET` was delayed ~90 minutes after publication.

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-11-10T23:39:01Z | #73 merge `2e868b1` |
| 2026-11-10T23:50:53Z | GitHub Release `v0.7.0` published |
| After that | `./release` had printed AWAIT publication |
| ~2026-11-11T01:18Z | Human manager: “how’s it going?” |

---

## 5. Mechanism on reproduction

**Confirmed.** `execute.sh` AWAIT branch exits 0 with resume text. Skill Step 6 has no subscribe/timer after that line. `gh release view v0.7.0` shows `publishedAt` 2026-11-10T23:50:53Z. A CI subscription on a branch named `v0.7.0` cannot observe that event.

---

## 6. The one thing

After `RELEASE:AWAIT publication`, the release skill must attach a wake that observes GitHub Release existence for that tag (Release event or timer that runs `gh release view`) and then re-invoke `./release`. A CI subscription on a branch with the tag’s name is not that wake.

---

## 7. Prevention test

If that wake had been in place, `./release` would have resumed when `v0.7.0` existed at 23:50:53Z and printed `RELEASE:MET` without a human poke. The ~90-minute silence could not have occurred.

---

## 8. Contributing factors

- AWAIT exits 0 (success), which looks like “done waiting” to a session that does not parse the resume sentence.
- Skill “do it” applies to closeout, not to polling publication.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | In `.agents/skills/release/SKILL.md`, after `RELEASE:AWAIT publication`, subscribe to GitHub Release for that tag (or a timer that checks `gh release view`) and resume `./release`. Document that `github:ci:branch` is not publication. |
| Owner | hub maintainer |
| Path | `.agents/skills/release/SKILL.md`; optionally `goals/hub_release/execute.sh` if the orchestrator should poll |
| Verification | A fixture AWAIT publication with an existing GitHub Release resumes to `RELEASE:MET` without a chat poke. |
| Implementation route | not in this record |

---

## 10. Follow-up

Detection-only “ask the human if stuck” is not the preventive action.
