# RCA: ship GO dumped a checklist instead of invoking `./release`

**Date:** 2026-11-11
**Queue id:** RCA-S02
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only.

---

## 1. Error condition

**Observed.** After the human manager authorized the `v0.7.0` cut, the producer session printed a human checklist (dispatch start-release, write notes, merge) instead of invoking `./release` from the repo root.

**Observed (skill).** [`.agents/skills/release/SKILL.md`](../../.agents/skills/release/SKILL.md) Step 6 is a single command fence: `./release`. The closeout section says do not dump steps on the user. [ADR 0038](../../adrs/0038-no-memory-in-process.md) forbids memory rituals.

**Not this record.** HTTP 403 on `gh workflow run` (RCA-S01). Empty Highlights after `./release` actually ran (RCA-S12).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | Chat | Human checklist instead of `Planner:` stdout |
| 3 | Producer session | Treated origin-line creation as a prerequisite *outside* `./release` |
| 2 | Skill Step 6 | Prose: run `./release`. No machine refuse when chat substitutes a list |
| 1 | `CREATE_RELEASE_LINE` | Local branch only; origin line is undocumented in the orchestrator (RCA-S01) |
| 0 | ADR 0038 / ADR 0049 | Process must own the next command; chat lists are not stops |

**Furthest controllable point:** after Ship: GO, the skill allows a producer session to emit instructions without `./release` stdout. Origin-line creation being outside the planner (S01) made that dump look necessary.

---

## 3. Impact / scope

The cut started with a human click list instead of one orchestrator invocation. Extra friction and a false new habit. `./release` was still the correct next command: it would have selected `CREATE_RELEASE_LINE` locally.

---

## 4. Timeline

| Time | Event |
| --- | --- |
| After pin-complete / ship authorization | Chat listed human steps instead of `./release` |
| After start-release run `42913807126` | `./release` later ran on `release/v0.7.0` |

---

## 5. Mechanism on reproduction

**Confirmed from skill bytes.** `git grep -n "dump steps" -- .agents/skills/release/SKILL.md` matches the closeout order. Step 6 is only `./release`. Nothing in `goals/hub_release/execute.sh` requires origin `release/v*` to exist before the first planner action.

---

## 6. The one thing

After Ship: GO, the producer session must invoke `./release` before any human instruction. The skill must state that a missing origin `release/v*` is not a reason to skip that command (planner owns that stop; see S01). A chat checklist between GO and `./release` is an incomplete skill execution.

---

## 7. Prevention test

If that order had been in place, the first post-GO bytes would have been `./release` stdout (`Planner: phase=… action=CREATE_RELEASE_LINE` or a named `HUMAN_DECISION`), not an Actions checklist. The 403 side-channel would not have been a substitute for the orchestrator.

---

## 8. Contributing factors

- S01: origin-line creation is not a planner action.
- Skill text already says do not dump steps; text without a refuse did not stop the dump (ADR 0038).

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | In `.agents/skills/release/SKILL.md` Step 6, state that `./release` is invoked even when origin `release/v*` is missing. Forbid any human checklist between Ship: GO and that command. Pair with S01 so the first stop is planner-owned. |
| Owner | hub maintainer |
| Path | `.agents/skills/release/SKILL.md` |
| Verification | `git grep` shows that sentence. A fixture skill that inserts an Actions checklist between GO and `./release` fails skill-author or a dedicated fitness. |
| Implementation route | not in this record |

---

## 10. Follow-up

Do not close S01 with this record. Origin-line dispatch remains S01.
