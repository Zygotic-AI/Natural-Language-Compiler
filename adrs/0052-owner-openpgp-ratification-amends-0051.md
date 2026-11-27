# ADR 0052 — Owner OpenPGP ratification (amends 0051)

- Status: Proposed
- Date: 2026-11-27
- Revision: 4
- Deciders: Human manager
- Class: F (integrity / hub produce)
- Corpus: nlc
- Decision-point: owner-openpgp-sidecar-format
- Amends: [ADR 0051](0051-hub-own-produce-principles.md) (SG2 ratification model)
- Supersedes in part: hash-only receipt semantics in [ADR 0047](history/0047-adr-approval-receipts-1.md) and the old gate-set receipt rows in ADR 0051 SG2. Hash-only receipt semantics in ADR 0047 and those gate-set rows are superseded in force.
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

RCA 5, root confirmed and remediation plan approved by the human manager 2026-10-11 (the RCA record is kept outside this repository): the two-actor principle (human manager ratifies, agents produce) was not carried into approval controls. Hash-only registries let producers rewrite stamps without the owner's act.

This record **amends policy** in ADR 0051: ratification is the human manager's **clearsigned approval statement** only. Private key stays on the owner's phone (PGPony). Agents commit pasted armor **unchanged**; they never create ratification.

Bootstrap trust anchor: owner Ed25519 public key, fingerprint **`9D1BD57770FC3A1DE84702750AFD22B063AE01BC`**, committed under `integrity/owner-keys/` with `integrity/owner-keys/TRUSTED_FINGERPRINTS`.

## Approval statement format (zyprompt-compatible)

Each ratification uses a **plain-text statement** (clearsigned in PGPony), with these fields:

```text
Repo: <org>/<repo>
Document: <repo-relative path>
Content-SHA256: <SHA-256 hex of document bytes exactly as committed>
Decision: <must match document Status line, e.g. Accepted>
Date: <YYYY-MM-DD>
Summary: <one line>
```

The signed artifact is committed **unchanged** beside the document:

```text
<document-path>.approval.asc
```

Example: `adrs/0052-owner-openpgp-ratification-amends-0051.md.approval.asc` next to this file.

**Zyprompt consistency:** The document **Status** line is **Accepted** when the sidecar is in force. Non-ADR Accepted documents need a sidecar `<document-path>.approval.asc` that is a valid clearsignature from a pinned fingerprint, whose Content-SHA256 equals the document bytes, and whose Decision equals Status (C6). Numbered ADRs use the same sidecar shape: **one signature per ADR**. Agents never write stamps (C8). The one **release** signature is a [ADR 0061](0061-release-in-seven-steps.md) checklist item, not this format’s second job.

## Decision

1. **Ratification SSOT:** Only the owner's clearsigned approval statement (format above) counts as ratification. No JSON hash row, registry field, or tool output substitutes.

2. **Pinned key:** Fingerprint `9D1BD57770FC3A1DE84702750AFD22B063AE01BC` is the in-force owner ratification key at adoption. Public key material lives in `integrity/owner-keys/richard-pickett.asc`; allowlist in `integrity/owner-keys/TRUSTED_FINGERPRINTS`.

3. **Key rotation / add:** A new fingerprint may enter `TRUSTED_FINGERPRINTS` only with a committed clearsigned statement **from a currently pinned key** authorizing the change, plus updated `.asc` if needed.

4. **Stamp / fitness (completion confirmation only):** Checks verify: (a) valid clearsignature from a pinned fingerprint; (b) **Content-SHA256** in the statement matches the document (or manifest) bytes in the tree; (c) **Decision** matches the document **Status**. Unsigned, wrong key, hash mismatch, tampered manifest, or **pending** → **NOT_MET**. **No tool may write a ratified entry.** Enforced for non-ADR Accepted documents by C6 (`fitness-adr-owner-sidecar`), C7 (`fitness-pending-ratification`), C8 (`fitness-no-tool-writes-ratification`), and for the gate-set batch by `fitness-gate-set-manifest`. **Release validate** (the release goal) fails an **Accepted** numbered ADR that has no verifying sidecar. Proposed ADRs do not need a sidecar. Pull-request CI does not require the private key ([ADR 0057](0057-tag-time-checker-digest.md)).

5. **Replace hash-only receipts:** The OpenPGP sidecar model replaces hash-only ADR 0047 JSON and ADR 0051 SG2 hash-only gate-set receipts. Gate-set batches use the signed manifest.

6. **PM independent verify:** At each review and release, the PM re-verifies signatures with an **out-of-repo copy** of the owner public key (not only CI), before treating ratification as real.

7. **Verifier implementation.** The Python-first hub verifier is in force (`tools/nouns/owner_sidecar/`): import key from `integrity/owner-keys/`, pin against `TRUSTED_FINGERPRINTS`, verify sidecars via GnuPG.

8. **Bootstrap:** First in-force ratification under this ADR is the owner's clearsigned statement for **this document** at PR head bytes, committed as this file's `.approval.asc`.

## Consequences

- ADR 0051 remains the property-goal law and is revised under [ADR 0059](0059-adr-revision-and-history.md).
- Version class **minor**.
- The verifier and gate-set manifest checks are in force.
- This ADR does **not** say that a release signature ratifies ADR bytes.

## Rejected

- Hash-only approval receipts as ratification evidence.
- Producer or maintainer tools that set ratified/pending registry state without a sidecar.
- Any retired or unpinned key fingerprint in `TRUSTED_FINGERPRINTS`.
- “The one release signature ratifies new ADR bytes.”

## Related

- [ADR 0051](0051-hub-own-produce-principles.md) — hub-own produce (amended in force by this record)
- [ADR 0047](history/0047-adr-approval-receipts-1.md) — prior hash receipt model (superseded)
- RCA 5 — kept outside this repository.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** owner sidecar; release-goal unsigned-Accepted gate. After accept: each Accepted ADR has `<path>.approval.asc`.
- **Adjectives that must hold:** agents never create armor; Accepted without sidecar fails release validate.
- **Non-goals:** digest membership (0057); staging activate (0055).
- **Tests:** `tools/fitness-adr-owner-sidecar.py`; release-goal gate `milestone` is 0061, unsigned-Accepted is this format.
- **Impact:** the owner signs each ADR once, then the release once.
