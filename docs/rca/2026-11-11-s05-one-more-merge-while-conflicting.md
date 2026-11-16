# RCA: merge-count given while the remaining ship PR was CONFLICTING

**Date:** 2026-11-11
**Queue id:** RCA-S05
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Do not fold RCA-S08 or RCA-S17 into this record.

---

## 1. Error condition

**Observed.** The human manager asked how many merges remained. The producer session counted one remaining merge (pull request #73, `release/v0.7.0` → `main`) while #73 was `CONFLICTING` against `main`. The next required merge was #74 into `release/v0.7.0`, then #73.

**Observed (GitHub).** #74 merged 2026-11-10T23:34:34Z (`d188058`, title “Merge main into release/v0.7.0 (keep v0.7.0 digest armor)”). #73 merged 2026-11-10T23:39:01Z (`2e868b1`, title “Release v0.7.0 (merge commit — do not squash)”). #73 body states PR 71 was squash-merged and `./release` will not tag a squash.

**Observed (skill).** [`.agents/skills/release/SKILL.md`](../../.agents/skills/release/SKILL.md) has no mergeability probe. `git grep` of that skill for `mergeable` / `CONFLICTING` is empty.

**Not this record.** Opening #73 before containment (RCA-S08). Existence of #74 (RCA-S17).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | Chat | “One more merge” while #73 could not merge |
| 3 | No `gh pr view --json mergeable,mergeStateStatus` | Count was memory, not GitHub state |
| 2 | Skill / offer path | Allows a remaining-click sentence without quoting mergeability |
| 1 | [ADR 0038](../../adrs/0038-no-memory-in-process.md) | Process must not substitute a remembered count for a live observation |
| 0 | [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) | Next stop is planner stdout, not a guessed merge tally |

**Furthest controllable point:** a merge-count sentence is legal in chat without a live `mergeable` observation on every cited pull request.

---

## 3. Impact / scope

The human manager was told the cut was one click away while GitHub would have refused that click. Extra question (“You want me to merge 74 first, then 73?”) and extra merge #74.

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-11-10T22:49:59Z | #71 squash `cc43f3e` |
| After #71, before #74 | #73 open and conflicting (digest armor hashes) |
| Chat | Remaining merges counted as one (#73) |
| 2026-11-10T23:34:34Z | #74 merged |
| 2026-11-10T23:39:01Z | #73 merged |

---

## 5. Mechanism on reproduction

**Confirmed.** Skill bytes contain no mergeability command. GitHub timestamps: #74 then #73. #73 title/body exist because squash + conflict were already known. A `CONFLICTING` pull request cannot be the sole remaining merge.

---

## 6. The one thing

A remaining-merge count may be spoken only after each cited pull request is observed `MERGEABLE` (`gh pr view --json mergeable,mergeStateStatus` or equivalent). The release skill must refuse a count (including “one more”) when any cited PR is `CONFLICTING`, and must quote that observation.

---

## 7. Prevention test

If that rule had been in place, the answer to “How many times do I need to merge?” would have been “#73 is CONFLICTING; next merge is not #73,” not “one more.” The error condition (a one-merge count while #73 conflicted) could not have been printed.

---

## 8. Contributing factors

- S08: #73 was offered before containment.
- S17: #74 existed only to clear that conflict.
- Jidoka (`.agents/instructions/jidoka-ssot-output.md`): do not counsel a step GitHub would refuse.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | In `.agents/skills/release/SKILL.md`, require a live mergeability observation before any remaining-merge count. `CONFLICTING` is not counted as a remaining merge. |
| Owner | hub maintainer |
| Path | `.agents/skills/release/SKILL.md` |
| Verification | `git grep mergeable` matches the skill. A fixture reply that counts a CONFLICTING PR as remaining fails skill-author or a dedicated fitness. |
| Implementation route | not in this record |

---

## 10. Follow-up

S08 and S17 stay open as separate error conditions.
