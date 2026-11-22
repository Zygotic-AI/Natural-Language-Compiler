# ADR 0059 — ADR revision and history

- Status: Accepted
- Date: 2026-11-07
- Revision: 1
- Deciders: Human manager
- Ratified-by: Human manager (ADR revision and history, 2026-11-07)
- Class: F (process)
- Corpus: nlc
- Amends: [ADR 0028](0028-closed-atomic-verb-set-and-policy-adr-lineage.md) (how a lineage tip is rewritten), [ADR 0029](0029-adr-lineage-active-set-and-bind-snapshot.md) (same number stays the name of the law)
- Related: charter R22 (superseded records are marked, not deleted)
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

Shadow records that say what an earlier accepted record “really means” are extra context. Current law should be one file. The past should be opt-in.

[ADR 0028](0028-closed-atomic-verb-set-and-policy-adr-lineage.md) already wanted only the tip active. It used a new ADR number as the mechanism. That leaves agents loading the old number and the new number to know what is in force.

## Decision

1. **Current law lives in `adrs/`.** Numbered files `adrs/NNNN-slug.md` are the only current records. The binder still reads only [`ACTIVE.md`](ACTIVE.md).

2. **Revision field.** Each current ADR has `Revision:` in the header, an integer starting at 1. A file with no field is revision 1.

3. **History folder.** Previous bytes live under `adrs/history/`. Scans of current law ignore that folder. The checker digest does not include it.

4. **Rewrite.** Before the current file is changed, copy it byte-for-byte to `adrs/history/NNNN-slug-R.md` where `R` is the previous revision (header if present, else 1). Then edit `adrs/NNNN-slug.md` and set `Revision:` to `R + 1`. Same number. Same path. The history file keeps the old name plus the old revision at the end.

5. **Revoked, superseded, rejected, removed.** Put that status in the header, then move the file to `adrs/history/` with the revision suffix. No current file remains in `adrs/`. [`INDEX.md`](INDEX.md) keeps the row and points at history. No stub in `adrs/`.

6. **Proposed.** A Proposed record may be edited in `adrs/` with no history copy. History starts when it is Accepted, or when it is rejected and moved.

7. **Sign independently.** The old bytes and the new bytes each get their own owner signature. An agent does not create those signatures. This record does not decide whether the branch suite verifies them; that stays [ADR 0056](0056-per-file-adr-detached-signatures.md) / [ADR 0057](0057-tag-time-checker-digest.md).

8. **New number means new decision.** A new `NNNN` is a different law, not a reword of an existing one.

## Consequences

- [ADR 0028](0028-closed-atomic-verb-set-and-policy-adr-lineage.md) decision 2 no longer requires a new number for a rewrite. The history copy is the immutable snapshot.
- [ADR 0053](history/0053-0051-0052-text-retrofit-1.md) (text retrofit) is rejected and moved to history. [ADR 0051](0051-hub-own-produce-principles.md) and [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md) are rewritten as revision 2.
- Charter R22 still holds: the trail is `adrs/history/`, not a second current file.

## Rejected

- A shadow ADR whose only job is the intended wording of another accepted ADR.
- Editing an accepted current file with no history copy.
- A stub in `adrs/` for a revoked record.
- Folding the 0056/0057 signing walk into this record.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** `adr_history` fitness. After accept: `adrs/history/`, header `Revision:`, current-law scans ignore history.
- **Adjectives that must hold:** current `adrs/NNNN-*.md` are not Rejected, Superseded, Revoked, or Removed; history filenames end in `-<revision>.md`.
- **Non-goals:** deciding branch vs tag signature checks (0056/0057); removing Cursor hooks (0058); bumping the shipped version.
- **Tests:** `tools/fitness-adr-history.py`; `tools/assert-adr-history-fails.py`.
- **Impact:** agents read one current file per decision; past bytes stay in `adrs/history/` when someone needs them.
