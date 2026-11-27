# Hub release

The hub release is an **executable goal** (`goals/hub_release/`). [ADR 0061](../../adrs/0061-release-in-seven-steps.md) is the readiness checklist that goal checks. This page explains; it does not copy the steps.

Unreleased work stays on `release/v*`. `main` is tagged production ([ADR 0044](../../adrs/0044-hub-release-production-trunk.md)). Agents load the steps from [`.agents/skills/release/SKILL.md`](../../.agents/skills/release/SKILL.md) and run the goal. `./release` is a thin entrypoint ([ADR 0048](../../adrs/0048-executable-shape.md)).

The first readiness gate asks whether every issue for this milestone is completed; it fails and names each open milestone issue. The goal takes the version from the `release/vX.Y.Z` branch name, not from `integrity/nlc-version.json`.

Release notes format: [`.agents/instructions/release-notes.md`](../../.agents/instructions/release-notes.md).
