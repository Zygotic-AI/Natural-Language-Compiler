# RCA: start-release origin line is not a planner action

**Date:** 2026-11-11
**Context:** Natural Language Compiler hub. Ship of `v0.7.0`. Queue id **RCA-S01**.
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard (`.agents/skills/planit/references/root-cause-analysis-standard.md`). This hub has no `/rca` SKILL.md; that standard is the runnable procedure.

**Scope (manifest):** Analysis only. New files `docs/rca/2026-11-11-s01-start-release-dispatch.md` and `docs/rca/2026-11-11-s01-start-release-dispatch.packet.json`. No workflow, planner, or skill change.

---

## 1. Error condition

**Observed.** A producer session ran `gh workflow run start-release` and GitHub returned HTTP 403 (`Resource not accessible by integration`). The session then instructed the human manager to open the Actions tab and dispatch **start-release** with version `v0.7.0`. The human manager treated that click as a new standing step.

**Observed (GitHub).** Workflow run `42913807126` (`start-release`, event `workflow_dispatch`, 2026-11-10T22:21:30Z, conclusion success) created `release/v0.7.0`. The triggering actor is the human manager GitHub identity. The previous successful dispatch (`42443051684`, 2026-11-08T03:31:07Z, `v0.6.0` line) has the same event and the same identity. No recorded `start-release` run in the last eight is an `workflow_dispatch` from a cloud-agent integration token.

**Observed (executor).** `CREATE_RELEASE_LINE` in `goals/hub_release/execute.sh` does not call `gh workflow run` and does not call `.github/workflows/start-release.yml`. On an absent local ref it runs `git checkout -b "${branch}"` only.

**Not this record.** Local `git checkout -b release/v0.7.0` succeeding. Tag publication. Extra pull-request merges (RCA-S03+).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | Chat | Instructed an Actions click after HTTP 403 |
| 4 | `gh workflow run start-release` | Side-channel dispatch. Cloud `GH_TOKEN` cannot `workflow_dispatch` (403) |
| 3 | `.agents/skills/release/SKILL.md` | Says run `./release`; do not dump steps. Did not name start-release as a planner stop |
| 2 | `goals/hub_release/execute.sh` `CREATE_RELEASE_LINE` | Creates a **local** `release/v*` ref. Does not create `origin/release/v*` |
| 1 | [`docs/adoption/RELEASE.md`](../adoption/RELEASE.md) | Origin `release/*` is created only via start-release, “from the Actions tab” |
| 0 | [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) | Every intentional stop must be a planner action. Origin-line creation is not one |

**Furthest controllable point:** origin `release/v*` creation is required by ruleset `25824126` (only the start-release app, id `5473379`, may create that ref) and is documented as a human Actions click, but it is not a planner `REPAIR` or `HUMAN_DECISION`. The producer session filled the gap with `gh workflow run` and then a chat checklist.

---

## 3. Impact / scope

The human manager had to dispatch start-release in the GitHub UI for `v0.7.0`, same as `v0.6.0`. The 403 did not change who can dispatch; it added a false “new habit” explanation. `./release` still cannot create `origin/release/v*` after this record.

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-11-08T03:31:07Z | start-release run `42443051684` success (`v0.6.0` line). `workflow_dispatch` by the human manager identity |
| 2026-11-10 | Producer session: `gh workflow run start-release` → HTTP 403 |
| 2026-11-10 | Chat asked for an Actions click with version `v0.7.0` |
| 2026-11-10T22:21:30Z | start-release run `42913807126` success. Same event and identity as `v0.6.0` |

---

## 5. Mechanism on reproduction

**Confirmed from bytes and GitHub, not re-run (dispatch would create another release line).**

1. `git grep -n "workflow run\\|start-release.yml" goals/hub_release/execute.sh` — executor has no dispatch.
2. `CREATE_RELEASE_LINE` branch: `git checkout -b` when `create_release_line_ref_state` is `absent`.
3. `gh api repos/Zygotic-AI/Natural-Language-Compiler/actions/runs/42913807126` — `event=workflow_dispatch`, triggering actor is the human manager identity.
4. Cloud-agent `gh workflow run` 403 is the documented GitHub restriction on integration tokens for `workflow_dispatch`.

---

## 6. The one thing

`CREATE_RELEASE_LINE` (or a dedicated planner action) must be the only origin `release/v*` creation path: either dispatch `.github/workflows/start-release.yml` with a token that can, or return `HUMAN_DECISION` whose remediation text is the existing Actions sentence in `docs/adoption/RELEASE.md`. A producer session must not call `gh workflow run` and must not invent a click list.

---

## 7. Prevention test

If that planner stop had been in place before `2026-11-10`, `gh workflow run start-release` would not have been a producer step, and the 403 could not have been translated into a new standing habit. The human manager would have seen one named `HUMAN_DECISION` quoting the Actions sentence already in `docs/adoption/RELEASE.md`, which is the same click that actually created run `42913807126`.

---

## 8. Contributing factors

- [`docs/adoption/RELEASE.md`](../adoption/RELEASE.md) already names the Actions tab. That sentence is correct for a human-only dispatch. It is not a planner stop, so a producer session can still run a side-channel command first.
- [ADR 0038](../../adrs/0038-no-memory-in-process.md) (no memory in process) forbids dumping a ritual the tools do not own. The skill already says do not dump steps; the missing origin-line action made the dump look necessary.
- Cloud-agent tokens cannot `workflow_dispatch`. That is why the side-channel 403ed. It is not why origin-line creation is outside `./release`.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Make origin `release/v*` creation a planner action: dispatch start-release when the token can, otherwise `HUMAN_DECISION` with the exact Actions sentence from `docs/adoption/RELEASE.md`. Remove any producer path that calls `gh workflow run` for this workflow. |
| Owner | hub maintainer |
| Path | `tools/nouns/release_state/release_state.py`, `goals/hub_release/execute.sh`, `.agents/skills/release/SKILL.md` |
| Verification | `git grep` of `execute.sh` shows start-release dispatch or a named `HUMAN_DECISION` for a missing origin `release/v*` ref. A specimen with no origin release line and a token that cannot dispatch prints that decision and does not print a free-form Actions checklist. |
| Human acceptance | not requested by this record |
| Implementation route | not in this record |

---

## 10. Follow-up

RCA-S02 (checklist instead of invoking `./release`) is a separate error condition. Do not close S02 with this record.
