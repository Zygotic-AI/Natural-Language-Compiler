# [ADR](../docs/TERMS.md#adr) 0019 — Guided orchestration (compile-guide kanban and resume)

- Status: Proposed
- Date: 2026-11-27
- Revision: 2
- Deciders: Human manager
- Class: F (product UX)
- Decision-point: compile-guide-kanban-resume
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

[ADR](../docs/TERMS.md#adr) 0017–0018 require human surfaces that **guide**, not manuals of steps. Exiting mid-flow must leave unfinished **interview / regen / ratify** work on `./nlc` and `/interview`. Release resume is not this ADR. Lifecycle state lives in document headers ([ADR 0064](0064-lifecycle-state-in-document-header.md)).

## Decision

1. **Primary human commands** stay short: `./nlc` (status + queue), `/interview` (guide), `/planit` (build & compile), `./nlc verify` (CI). The short command list **points at** [ADR 0020](0020-human-vs-agent-commands.md). Agents run `./nlc maintainer requirements` after ratification.
2. **`./nlc` preflight:** [Verify](../docs/TERMS.md#verify) install and skills before showing the queue. On failure, stop with **problem + fix** (e.g. `./nlc doctor fix`), per [ADR](../docs/TERMS.md#adr) 0018.
3. **Queue is kanban:** **`/interview` is always-on guide** (not a bucket). Work flows **Requirements → Build & compile → [Verify](../docs/TERMS.md#verify)** (then Maintain). Requirements covers new, updated, and unfinished work (including proposed ADRs) — all before compile. [Verify](../docs/TERMS.md#verify) means prod-ready: requirements ratified and applied, generated goals complete. The queue is a **scan of document headers** ([ADR 0064](0064-lifecycle-state-in-document-header.md)). This ADR does not authorize `.nlc/work-queue.json`, `.nlc/pipeline-state.json`, `.nlc/requirements-sync-pending.json`, or `.nlc/last-requirement-change.json`.
4. **Requirements path:** `/interview` drafts and ratifies. Agent runs `./nlc maintainer requirements` (checks + optional regen from the session document headers).
5. **Resume:** Any in-flight **ratification, regen queue, or guide session** appears on `./nlc` and should be picked up by `/interview` (“continue unfinished work or start something new?”). This is not release resume. Release resume belongs on the **release goal**.

## Consequences

- [`tools/nlc_requirements_cmd.py`](../tools/nlc_requirements_cmd.py) and `./nlc requirements` replace advertising `check-rules` / `regen-plan` on the short menu.
- Maintainer tools stay; humans are not trained on their names first.

## Rejected

- Long menu copy on default `./nlc` output.
- Expecting adopters to run `regen-plan` manually after every policy change.
- Release steps or release resume in this record.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** dashboard; compile-guide session document. After accept: queue from headers.
- **Adjectives that must hold:** those four JSON names are not lifecycle SSOT.
- **Non-goals:** release goal; type walk (0065).
- **Tests:** `tools/fitness-guide-orchestration.py`.
- **Impact:** unfinished interview/regen/ratify still shows on `./nlc`.
