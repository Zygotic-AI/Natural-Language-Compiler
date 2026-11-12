# FEATURES-DRAFT-NOVEMBER

Temporary draft. Not yet integrated into FEATURES.md. Created 2026-11-11.

---

## Planet Tenets

1. **Everything produced gets an audit.** Any artifact Planet builds is followed by an audit that confirms it was produced correctly.

2. **Every artifact ships with a JSON manifest.** The manifest accompanies the work product and describes it.

3. **The audit consumes both.** The post-production audit receives the manifest and the work product, and uses both to verify correctness.

4. **One run-level index JSON.** When Planet is executed, it creates a single JSON that either contains or indexes all the manifest JSONs produced during that run.

5. **ADR binding records decisions.** When ADRs are bound, Planet lists every ADR it considered applicable and writes a decision record for each one into the JSON manifest, indicating why it decided to keep or refuse it.

6. **Model-call accounting.** Every model call records the model, the provider, the harness in use, tokens consumed, and cost when the model returns it. A reserved slot holds accounting data even when the model does not return it.

---

## Observability Additions (Run-Level)

These belong on the run-level JSON, not on every model call. The per-call record stays lean: model, provider, harness, tokens, cost, accounting slot.

- **Timestamps with durations** on every step, so a run's timeline can be reconstructed.
- **Parent-child run ID**, so nested or sub-agent executions link back to the top-level trigger.
- **Environment fingerprint** — OS, dependency versions, pinned model versions at build time — so a build is reproducible later.
- **Input hashes** of the exact inputs: the prompt, the policy text, the ADRs considered.
- **Human actor** on every approval or refusal, not just the system decision. The item auditors ask for first.

---

## RCA Manifest Requirement

Root-cause analysis (RCA) also produces a record artifact (docs/rca or draft/rca on non-trivial failures). RCA needs the same manifest-and-accounting treatment as the other inference-backed producers.

---

## Inference-Backed Producers Needing Manifest Treatment

Confirmed from skill frontmatter (model invocation enabled): proposer, reviewer, confirmer, recorder, planit.

Planit is the sole documented caller of the leaf skills. RCA is a procedure planit invokes on its failure path (step nine), not a model-invocation-enabled skill in its own right, but it still emits a record artifact.

Clear inference-backed producers: **audit, adopt, policy ingest**. Verify-deep may qualify depending on whether it uses an LLM for deeper analysis. Impact analysis, rule conflict detection, and basic verify are deterministic (graph walks, rule matching) and do not need this treatment.
