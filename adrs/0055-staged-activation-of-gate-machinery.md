# ADR 0055 — Staged activation of gate machinery

- Status: Proposed
- Date: 2026-11-27
- Revision: 4
- Deciders: Human manager
- Class: F (integrity / hub produce)
- Decision-point: staged-gate-activation
- Related: [ADR 0046](history/0046-repository-planit-identity-1.md) (repository Planit identity, rejected), [ADR 0051](0051-hub-own-produce-principles.md) (hub-own produce), [ADR 0052](0052-owner-openpgp-ratification-amends-0051.md) (owner OpenPGP ratification), [ADR 0054](0054-published-skill-author-contract.md) (published-skill author contract)
- Version class of this change: **minor** (new policy; not a published-contract break)

## Context

The 2026-10-25 unregistered Planit skill land showed four stacked failures: Skill produce treated one author checklist as done; owner-signature and identity mandates were after-the-fact detectors; the live gating skill was both the mandated artifact and the machinery that must load to ingest a signature; and signing design never required a create–change–sign–ingest–rotate walkthrough or a known-bad of a legitimate verifier change.

Owner-approved remediation (2026-10-24 / 2026-10-25): members of the self-referential set change only through a staging area. The live signed machinery verifies the staged candidate and the owner's signature. One activation commit moves staged bytes into live paths together with the regenerated registry, install hashes, manifest, and the owner's sidecar — or nothing lands.

The product owner: tools are staged and swapped under the **one release signature**. There is no per-tool signature. “I don't need to sign all the tools.”

## Decision

1. **Derived self-referential set.** Membership is computed by `python3 tools/derive-self-ref-set.py` from role detectors (gating skills, owner hook, identity tool and registry, gate-set membership derivation, manifest generator, sidecar verifier, C8, owner keys, install hashes, and the staging/activation tools themselves). The list is not hand-kept. Snapshot: `integrity/self-ref-set.json`.

2. **Staging area.** Candidates live under `staging/<change-id>/` mirroring live paths. That prefix is excluded from `derive_gate_set_paths`. Staging is a candidate, not a loadable Planit skill.

3. **Live verifier stays live.** The previously signed live `/planit`, hook, identity tool, sidecar verifier, and owner keys verify the staged candidate. The staged skill is never loaded as `/planit`.

4. **Atomic activate.** `python3 tools/activate-gate-machinery.py --change-id <id>` (and `--armor` only when the owner pasted armor for a non-release path that still uses a sidecar) swaps staged bytes into live paths together with the regenerated Planit registry (from bytes), install hashes, and the proposed manifest. It never creates a signature. **Activate has no signature of its own.** The swap is covered by the **one release signature** ([ADR 0061](0061-release-in-seven-steps.md)).

5. **Live-member refuse.** Any change to a live self-ref member outside an activation commit is refused at produce time and by `python3 tools/fitness-live-self-ref-activation.py`. The first land of this machinery is the **bootstrap** activation (this record + tools + regenerated pins). After those tools exist on the base, bootstrap is not available.

6. **Mandate inheritance.** `python3 tools/derive-mandated-paths.py` is the one derived list of mandated paths. The Skill type recipe, the skill-author checklist (`mandate-pins`), and the release skill import it. Touching a listed path without moving its pins in the same change is a produce-time refuse. A regenerated-but-unsigned manifest is **INCOMPLETE** produce, not a finished step.

7. **Control-design process.** Planit and the briefing standard require, for any control or gate design, a full lifecycle walkthrough and a known-bad of **legitimate change to the verifier** that must succeed through staging. Those are checked rules (`CONTROL-LIFECYCLE`), not prose only.

## Lifecycle walkthrough (create, change, sign, ingest, rotate, first bootstrap)

### Create (new self-ref member)

1. Author candidate bytes under `staging/<change-id>/` mirroring the intended live path (`python3 tools/stage-gate-machinery.py --change-id <id> --path <live-rel>` then edit the staged copy).
2. Live `/planit` still matches the registry. Owner prompts and Planit intake pass.
3. Live generator computes the proposed gate-set manifest with staged overrides. Do not mark produce done.
4. Activate under the release that carries the one release signature: live verifier checks proposed bytes; one commit swaps bytes + registry + install hashes + manifest.
5. After that commit the hook, Planit identity, install-verify, and sidecar P1 go green together.

### Change (existing live member)

Same as create, except stage copies the current live file first. Editing the live path directly is a produce-time and fitness refuse.

### Sign

The owner signs the **release** ([ADR 0061](0061-release-in-seven-steps.md)), not each tool. Signing does not need `/planit`.

### Ingest

The activate tool is the ingest path. It swaps staged bytes. A split land (bytes, then sidecar later) is refused.

### Rotate (owner key)

Key rotation stays ADR 0052 decision 3: a currently pinned key authorizes a new fingerprint. The key material and `TRUSTED_FINGERPRINTS` are self-ref members. Stage the key change, then activate under the release signature. A manifest signed only by the new unlisted key is NOT_MET.

### First bootstrap (this activation)

The staging prefix, activate tool, derived-set generator, mandate list, and this record cannot be staged by machinery that does not yet exist. After those tools exist on the release-line base, further self-ref edits use staging + activate only.

## Consequences

- Version class **minor**.
- C8 is unchanged: no tracked tool writes a created `*.approval.asc`.
- The live Planit registry is generated from skill bytes. Hand-bumping the registry to pass the hook is refused.

## Rejected

- Per-tool signatures.
- Bumping the live Planit registry so the hook passes, then signing later (RCA 5 / ADR 0052).
- Disabling or bypassing the identity hook to deliver a sidecar (ADR 0046).
- A second loadable Planit skill name for staging.
- Hand-kept self-ref or mandated-path lists.

## Related

- RCA 2026-10-25 unregistered Planit skill edit (Climbs 1–4), kept on `rca/planit-unregistered-skill-edit`.

## Proposal (G-PROPOSE)

- **Change class:** F
- **Nouns / verbs / goals touched:** staging/activate. After accept: activate has no own armor.
- **Adjectives that must hold:** live self-ref edits outside activate refuse; no per-tool signature required.
- **Non-goals:** sidecar format (0052); digest (0057).
- **Tests:** `tools/fitness-live-self-ref-activation.py`; `tools/assert-live-self-ref-direct-edit-fails.py`.
- **Impact:** tools swap under the release signature.
