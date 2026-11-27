# ADR 0057 — One tag-time signature over the checker digest

- Status: Accepted
- Date: 2026-10-31
- Revision: 2
- Amended-by: [ADR 0061](0061-release-in-seven-steps.md) (revision 2)
- Deciders: Human manager
- Ratified-by: Human manager (tag-time checker digest, 2026-11-07)
- Class: F (integrity / hub produce)
- Corpus: nlc
- Supersedes in part: [ADR 0056](history/0056-per-file-adr-detached-signatures-1.md) (per-file ADR signatures are not a branch or tag requirement)
- Amends: [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md) (when the owner signature is required)
- Related: [ADR 0055](0055-staged-activation-of-gate-machinery.md)

## Context

The hub asked the owner to clearsign a 3,627-row gate-set manifest on every branch, and to detached-sign each Accepted architecture decision as well. Those decision records were already rows in the manifest, so each one was signed twice. [ADR 0056](history/0056-per-file-adr-detached-signatures-1.md) names the per-file shape. This record says those files are not a branch or tag requirement. A one-line instruction file was enough to void the manifest and turn the pull-request suite red.

The threat that remains is an agent editing the code that decides pass/fail and then reporting that the edit passed. One owner signature over those bytes, checked at tag time by the checker already on `main`, stops that. A pull request does not need the private key.

Version class of this change is **major**: it removes the per-file signature obligation and the mid-branch clearsign obligation.

## Decision

1. **Signed set.** The owner signs one document, `integrity/checker-digest.sha256`. Its bytes are the sha256 of a canonical listing of: checker programs (`tools/ci_fitness.py`, `tools/fitness-*.py`, `tools/assert-*.py`, and the checker nouns named in `tools/nouns/checker_digest/checker_digest.py`), and numbered records `adrs/NNNN-*.md`. Examples, generated ledgers, and instruction files are not in that listing. A listed path that is not a pass/fail input is a defect in the rule. A listed path that no longer exists (`.github/workflows/fitness.yml`, deleted by ADR 0061) is skipped.

2. **Validate.** `./release validate` runs the suite once and checks that the digest file matches the tree. It does not require `integrity/checker-digest.sha256.approval.asc`. It does not require `adrs/*.md.asc`. It does not require the gate-set manifest sidecar.

3. **Tag.** `./release tag` refuses to tag until the digest signature verifies. The verifier is `tools/check-checker-digest-signature.py` from the previous release tag, with that tag's `integrity/owner-keys/`, run against `origin/main`. The commit being tagged is never its own verifier. A key added in a release is trusted from the next release.

4. **One regenerator.** `python3 tools/regen-derived-release-state.py` rewrites the digest, the gate-set manifest, mandated paths, the self-ref snapshot, install hashes, and the hub content-tree digest. The suite reports drift of those files as one check, `fitness-derived-release-state`. `./release validate` runs the regenerator before the suite.

5. **Product ship.** `Released-by:` on `CONFIRM.md`, checked by `tools/release-audit.py`, is unchanged.

## Lifecycle (create, change, sign, ingest, rotate, first bootstrap)

### Create

The digest file is written by the regenerator. No signature is created by a tool.

### Change

A checker, workflow, or numbered decision-record edit changes the digest. `./release validate` rewrites the digest file before the suite runs. The release branch needs no armor until step 4.

### Sign

The owner clearsigns `integrity/checker-digest.sha256` with the pinned key. The statement's Content-SHA256 is the sha256 of that file.

### Ingest

The armor is `integrity/checker-digest.sha256.approval.asc`. `./release tag` ingests it by running the previous release tag's checker with that tag's owner keys. A legitimate change to the verifier stays machine-testable on the branch without a signature, and the tag refuses until the previous tag's checker accepts the armor. The new verifier does not accept its own signature.

### Rotate

Key rotation stays ADR 0052 decision 3. A fingerprint added in a release is trusted from the next release's tag (decision 3). A digest signed only by an unlisted key is NOT_MET.

### First bootstrap

Every release tag from v0.8.0 on contains `tools/check-checker-digest-signature.py`. `./release tag` refuses when there is no previous release tag.

## Consequences

- Per-file `adrs/*.md.asc` files may remain in history. The suite does not read them.
- The gate-set manifest remains a machine membership list. Its sidecar is not a branch gate.
- The next hub ship that tags this rule is a **major** version.

## Rejected

- Keeping a per-file detached signature for every Accepted decision record.
- Requiring the owner signature before a pull request can be green.
- Letting the commit being tagged run its own signature check.

## Related

- [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md)
- [ADR 0055](0055-staged-activation-of-gate-machinery.md)
- [ADR 0056](history/0056-per-file-adr-detached-signatures-1.md)
