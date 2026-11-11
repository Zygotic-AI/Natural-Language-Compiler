# RCA: ship PR to main opened before tag-time checker-digest signature

**Date:** 2026-11-11
**Queue id:** RCA-S07
**Status:** open (RCA only; no remediation in this record)
**Skill:** Planit RCA standard. No `/rca` SKILL.md in this hub.

**Scope (manifest):** Analysis only. Do not fold RCA-S16 into this record.

---

## 1. Error condition

**Observed.** Planner `ALIGN_VERSION` runs `python3 tools/nlc_release_bump.py --align-to "${desired}"` (`goals/hub_release/execute.sh`). That regenerates `integrity/checker-digest.sha256`. Pull request #71 (`release/v0.7.0` → `main`) opened and merged 2026-11-10T22:49:59Z as `cc43f3e` while `integrity/checker-digest.sha256.approval.asc` still signed the previous digest.

**Observed (history).** Armor commit `bd50f45` (“chore: ratify checker digest for v0.7.0 tag”) is not an ancestor of `cc43f3e`. It landed via pull request #72 (merged 2026-11-10T23:23:41Z). [ADR 0057](../../adrs/0057-tag-time-checker-digest.md) requires the owner clearsign at tag time; [`tools/nlc_release_tag_gate.py`](../../tools/nlc_release_tag_gate.py) calls `tools/check-checker-digest-signature.py`.

**Observed (offer).** `CREATE_PR` and `tools/pr-offer-gate.py` do not require `CHECKER_DIGEST_SIGNATURE:MET` on the candidate. Tag gate runs later, at `CREATE_LOCAL_TAG`.

**Not this record.** Signature arriving in #72 (RCA-S16). “Tag next” after #71 (RCA-S04).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | #71 | Ship PR to `main` without current armor |
| 3 | CREATE_PR / pr-offer-gate | Offer to `main` with no signature check |
| 2 | ALIGN_VERSION | New digest bytes; armor now stale |
| 1 | Tag gate | Signature is checked only at tag |
| 0 | ADR 0057 / ADR 0049 | Tagged commit must carry armor; no planner action “signature current before OPEN_PR_TO_MAIN” |

**Furthest controllable point:** a `release/v*` → `main` offer is legal while `check-checker-digest-signature.py` is NOT_MET.

---

## 3. Impact / scope

#71 could not be tagged even if it had been a merge commit. The owner was asked to sign after a ship PR already existed. Extra PR #72 followed (S16).

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| Before #71 | ALIGN_VERSION regenerated digest |
| 2026-11-10T22:49:59Z | #71 merged `cc43f3e` (v0.6.0 armor still on tree) |
| 2026-11-10T23:23:41Z | #72 merged (v0.7.0 armor `bd50f45`) |

---

## 5. Mechanism on reproduction

**Confirmed.** `git merge-base --is-ancestor bd50f45 cc43f3e` is false. Tag gate script list includes `check-checker-digest-signature.py`. `git grep -n checker-digest -- tools/nouns/pr_offer_gate.py` comments that digest members are unchanged so the signature stays valid — it does not *check* the signature. CREATE_PR body/path has no signature probe.

---

## 6. The one thing

A ship PR (`release/v*` → `main`) must not be offered unless `python3 tools/check-checker-digest-signature.py` is MET on that HEAD. CREATE_PR / pr-offer-gate must refuse otherwise. The owner-signature HUMAN_DECISION belongs before that offer.

---

## 7. Prevention test

If that refuse had been in place, #71 could not have opened while armor still covered v0.6.0 bytes. The error condition (ship PR before tag-time signature) could not have occurred.

---

## 8. Contributing factors

- Human-only signature is correct; **when** it is requested is the defect (S16).
- ALIGN_VERSION progress fact is `worktree_file_version` only, not armor-current.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | CREATE_PR and `tools/pr-offer-gate.py` refuse `release/v*` → `main` unless `check-checker-digest-signature.py` is MET on the candidate HEAD. |
| Owner | hub maintainer |
| Path | `goals/hub_release/execute.sh` CREATE_PR; `tools/pr-offer-gate.py`; planner facts |
| Verification | A fixture HEAD with stale armor cannot print `PR_OFFER_GATE:MET` or run `gh pr create` to `main`. |
| Implementation route | not in this record |

---

## 10. Follow-up

S16 is the late landing of the armor, not this offer.
