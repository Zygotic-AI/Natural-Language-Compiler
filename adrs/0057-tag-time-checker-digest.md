# ADR 0057 — One tag-time signature over the checker digest

- Status: Proposed
- Date: 2026-11-27
- Revision: 3
- Deciders: Human manager
- Class: F (integrity / hub produce)
- Corpus: nlc
- Decision-point: tag-time-checker-digest
- Supersedes in part: [ADR 0056](history/0056-per-file-adr-detached-signatures-1.md) (per-file ADR signatures are not a **pull-request** requirement)
- Amends: [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md) (when the owner signature is required)
- Related: [ADR 0055](0055-staged-activation-of-gate-machinery.md)
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

The hub asked the owner to clearsign a 3,627-row gate-set manifest on every branch, and to detached-sign each Accepted architecture decision as well. A pull request does not need the private key. The threat that remains is an agent editing the code that decides pass/fail and then reporting that the edit passed. One owner signature over those bytes, checked at tag time by the checker already on `main`, stops that.

Revision 2 said validate does not require ADR signatures. That sentence is dropped. **Release validate** fails an Accepted ADR with no verifying sidecar ([ADR 0052](0052-owner-openpgp-ratification-amends-0051.md)). Pull-request CI still does not require the private key.

## Decision

1. **Signed set.** The owner signs one document, `integrity/checker-digest.sha256`. Its bytes are the sha256 of a canonical listing of: checker programs (`tools/ci_fitness.py`, `tools/fitness-*.py`, `tools/assert-*.py`, and the checker nouns named in `tools/nouns/checker_digest/checker_digest.py`), and numbered records `adrs/NNNN-*.md`. Examples, generated ledgers, and instruction files are not in that listing. A listed path that is not a pass/fail input is a defect in the rule. A listed path that no longer exists (`.github/workflows/fitness.yml`, deleted by ADR 0061) is skipped.

2. **Validate.** The **release goal**’s validate step runs the suite once and checks that the digest file matches the tree. It **does** fail when an **Accepted** numbered ADR has no verifying `<path>.approval.asc` ([ADR 0052](0052-owner-openpgp-ratification-amends-0051.md)). It does not require `integrity/checker-digest.sha256.approval.asc` until sign. It does not require the gate-set manifest sidecar on the branch. Proposed ADRs do not need sidecars.

3. **Tag.** `./release tag` refuses to tag until the digest signature verifies. The verifier is `tools/check-checker-digest-signature.py` from the previous release tag, with that tag's `integrity/owner-keys/`, run against `origin/main`. The commit being tagged is never its own verifier. A key added in a release is trusted from the next release.

4. **One regenerator.** `python3 tools/regen-derived-release-state.py` rewrites the digest, the gate-set manifest, mandated paths, the self-ref snapshot, install hashes, and the hub content-tree digest. The suite reports drift of those files as one check, `fitness-derived-release-state`. Validate runs the regenerator before the suite.

5. **Product ship.** `Released-by:` on `CONFIRM.md`, checked by `tools/release-audit.py`, is unchanged.

## Lifecycle (create, change, sign, ingest, rotate, first bootstrap)

### Create

The digest file is written by the regenerator. No signature is created by a tool.

### Change

A checker, workflow, or numbered decision-record edit changes the digest. Validate rewrites the digest file before the suite runs.

### Sign

The owner clearsigns `integrity/checker-digest.sha256` with the pinned key. The statement's Content-SHA256 is the sha256 of that file. That is the **one release signature**.

### Ingest

The armor is `integrity/checker-digest.sha256.approval.asc`. `./release tag` ingests it by running the previous release tag's checker with that tag's owner keys.

### Rotate

Key rotation stays ADR 0052 decision 3. A fingerprint added in a release is trusted from the next release's tag (decision 3).

### First bootstrap

Every release tag from v0.8.0 on contains `tools/check-checker-digest-signature.py`. `./release tag` refuses when there is no previous release tag.

## Consequences

- Per-file `adrs/*.md.asc` / `.approval.asc` files may remain in history. Pull-request CI does not require them. Release validate requires `.approval.asc` on **Accepted** ADRs.
- The gate-set manifest remains a machine membership list. Its sidecar is not a branch gate.

## Rejected

- “Validate does not require ADR signatures” as a standing sentence.
- Requiring the owner private key before a pull request can be green.
- Letting the commit being tagged run its own signature check.

## Related

- [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md)
- [ADR 0055](0055-staged-activation-of-gate-machinery.md)
- [ADR 0056](history/0056-per-file-adr-detached-signatures-1.md)

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** release-goal unsigned-Accepted gate; digest regenerator. After accept: PR green without owner key; release validate names unsigned Accepted ADRs.
- **Adjectives that must hold:** tag still uses the previous tag’s checker; PR suite does not require digest armor.
- **Non-goals:** sidecar format (0052).
- **Tests:** `tools/fitness-derived-release-state.py`; `tools/assert-tag-digest-signature-required-fails.py`.
- **Impact:** the owner signs ADRs when they become Accepted, then signs the release.
