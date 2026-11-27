# ADR 0059 — ADR revision, history, and status words

- Status: Proposed
- Date: 2026-11-27
- Revision: 3
- Deciders: Human manager
- Class: F (process)
- Corpus: nlc
- Decision-point: adr-revision-history-status-words
- Related: charter R22 (superseded records are marked, not deleted)
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

Shadow records that say what an earlier accepted record “really means” are extra context. Current law should be one file. The past should be opt-in. The in-force word is **Accepted** everywhere. Where that word sits (the header) is [ADR 0064](0064-lifecycle-state-in-document-header.md). This ADR is the **words**, the history copy/move, and that Accepted means constraints built plus the ADR’s own signature.

## Decision

1. **Current law lives in `adrs/`.** Numbered files `adrs/NNNN-slug.md` are the only current records. The binder still reads only [`ACTIVE.md`](ACTIVE.md) ([ADR 0029](0029-adr-lineage-active-set-and-bind-snapshot.md)).

2. **Revision field.** Each current ADR has `Revision:` in the header, an integer starting at 1. A file with no field is revision 1.

3. **History folder.** Previous bytes live under `adrs/history/`. Scans of current law ignore that folder. The checker digest does not include it.

4. **Rewrite.** Before the current file is changed, copy it byte-for-byte to `adrs/history/NNNN-slug-R.md` where `R` is the previous revision (header if present, else 1). Then edit `adrs/NNNN-slug.md` and set `Revision:` to `R + 1`. Same number. Same path. The history file keeps the old name plus the old revision at the end.

5. **Revoked, superseded, rejected, removed.** Put that status in the header, then move the file to `adrs/history/` with the revision suffix. No current file remains in `adrs/`. [`INDEX.md`](INDEX.md) keeps the row and points at history. No stub in `adrs/`.

6. **Proposed.** A Proposed record may be edited in `adrs/` with no history copy. History starts when it is Accepted, or when it is rejected and moved. Agents never write approval stamps.

7. **Accepted.** The only in-force status word is **Accepted**. Proposed, Superseded, and Rejected stay. **Accepted** means: constraints built ([ADR 0062](0062-constraint-stack.md)) and human accept recorded by **this ADR’s own** OpenPGP sidecar ([ADR 0052](0052-owner-openpgp-ratification-amends-0051.md)). This ADR does **not** say that a release signature ratifies new ADR bytes. The one release signature is [ADR 0061](0061-release-in-seven-steps.md).

8. **New number means new decision.** A new `NNNN` is a different law, not a reword of an existing one. Overlap of names is [ADR 0063](0063-adr-decision-point-register.md).

9. **TODO is not a status source.** INDEX, CATALOG, ACTIVE, and the file header are the status sources. [`TODO`](../TODO) is a task queue.

## Consequences

- [ADR 0028](0028-closed-atomic-verb-set-and-policy-adr-lineage.md) no longer owns copy/move.
- [ADR 0029](0029-adr-lineage-active-set-and-bind-snapshot.md) displays Accepted for in-force; it does not invent a second vocabulary.
- Charter R22 still holds: the trail is `adrs/history/`, not a second current file.

## Rejected

- A shadow ADR whose only job is the intended wording of another accepted ADR.
- Editing an accepted current file with no history copy.
- A stub in `adrs/` for a revoked record.
- “The one release signature ratifies new ADR bytes.”
- Amend-without-edit (a note that changes law without changing the current file).

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** `adr_history` fitness. After accept: Accepted = sidecar + constraints built.
- **Adjectives that must hold:** current `adrs/NNNN-*.md` are not Rejected, Superseded, Revoked, or Removed; history filenames end in `-<revision>.md`.
- **Non-goals:** sidecar format (0052); header location (0064).
- **Tests:** `tools/fitness-adr-history.py`; `tools/assert-adr-history-fails.py`.
- **Impact:** agents read one current file per decision; past bytes stay in `adrs/history/`.
