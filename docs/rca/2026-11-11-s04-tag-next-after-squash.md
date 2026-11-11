# RCA: “next step is the tag” after a non-taggable merge

**Date:** 2026-11-11
**Queue id:** RCA-S04
**Status:** open (RCA only)
**Skill:** Planit RCA standard.

**Scope (manifest):** Analysis only.

---

## 1. Error condition

**Observed.** After PR #71 merged, the producer session told the human manager the next step was the tag. Two independent tag-gate facts were already false:

1. `cc43f3e` has one parent (not a merge commit). [`nlc_release_context.py`](../../tools/nouns/nlc_release_context/nlc_release_context.py) treats that as `not_contained`.
2. `integrity/checker-digest.sha256.approval.asc` on that commit still covered **v0.6.0** bytes. Tag gate [`nlc_release_tag_gate.py`](../../tools/nlc_release_tag_gate.py) `checker_digest_signature_problems` refuses.

**Observed.** PR #71 body: “After merge, `./release` tags **v0.7.0** on that merge commit.” That sentence was written *before* merge, then reused as if the tag gate had passed.

**Not this record.** Opening #71 before the signature existed (RCA-S07). The squash object itself (RCA-S15).

---

## 2. Upstream chain

| Step | Producer | What it did |
| --- | --- | --- |
| Symptom | Chat | Promised a tag |
| 3 | Offer body | Pre-committed “after merge, tag” |
| 2 | No re-read of tag-gate facts | `./release` was not invoked to print `RELEASE:NOT_MET` |
| 1 | Tag gate + containment | Would have refused `cc43f3e` |
| 0 | [ADR 0049](../../adrs/0049-release-planner-owns-stops.md) / jidoka | Next step must come from planner stdout |

**Furthest controllable point:** a ship-PR offer prints an unconditional “tag after merge” sentence. Nothing re-runs the tag gate before that sentence is used as the next human instruction.

---

## 3. Impact / scope

The human manager believed the cut was one merge from a tag. It was not. Extra PRs #72–#74 followed.

---

## 4. Timeline

| Time (UTC) | Event |
| --- | --- |
| 2026-11-10T22:49:59Z | #71 squash `cc43f3e` |
| After that merge | Chat: tag is next |
| 2026-11-10T23:39:01Z | #73 merge commit `2e868b1` actually tagged |

---

## 5. Mechanism on reproduction

**Confirmed.** `git log -1 --format=%P cc43f3e` → one parent. Armor at `cc43f3e` is not `bd50f45` (signature commit on the later line). `python3 tools/nlc_release_tag_gate.py --check --commit cc43f3e --tag v0.7.0` is the command that must be NOT_MET (signature and/or identity). Containment: `len(fields) < 3` → “is not a merge commit”.

---

## 6. The one thing

The only sentence that may tell a human the tag is next is `./release` stdout after the tag gate is MET on the merge SHA. Offer bodies must not promise a tag. A producer session must invoke `./release` after the ship PR merges and quote `RELEASE:NOT_MET` when the gate refuses.

---

## 7. Prevention test

If that rule had been in place, the post-#71 message would have been tag-gate / containment `NOT_MET`, not “tag next.” The human manager would not have been told the cut was done.

---

## 8. Contributing factors

- Jidoka instruction (`.agents/instructions/jidoka-ssot-output.md`): do not counsel a step the gates refuse.
- S07: signature was not on #71.
- S15: squash made containment false.

---

## 9. Preventive action

| Field | Value |
| --- | --- |
| Action | Forbid “tag after merge” in CREATE_PR / offer bodies. After a ship PR merges, the only next instruction is `./release` quoted stdout. |
| Owner | hub maintainer |
| Path | `goals/hub_release/execute.sh` CREATE_PR body; `.agents/skills/release/SKILL.md` await-merge path |
| Verification | `git grep` of CREATE_PR body has no “tags v”. A fixture offer body that promises a tag fails fitness. |
| Implementation route | not in this record |

---

## 10. Follow-up

S07 (signature before ship PR) and S15 (squash) remain separate.
