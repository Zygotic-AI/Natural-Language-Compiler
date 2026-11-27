# Hub release goal

The thin entrypoint is `./release` (`scripts/nlc-release.sh`). This goal owns the machine: ADR 0061 checklist, resume, record, then validate/sign/main/tag.

## How the goal determines the release version (the branch)

The product owner (2026-11-27 5:19 PM CT): “clearly define how it can determine that branch.”

- The release goal reads the branch it is run on: `git rev-parse --abbrev-ref HEAD`. In GitHub Actions, where HEAD is detached, it reads `GITHUB_REF_NAME` instead.
- That name must match exactly `^release/v(\d+)\.(\d+)\.(\d+)$`. The captured vX.Y.Z is the version being released.
- Any other result (main, a change branch, detached HEAD with no ref name) refuses, saying which branch it saw and that a release runs only on release/vX.Y.Z.
- Milestone: exactly one GitHub milestone (any state) whose title ends with " - vX.Y.Z". Zero or more than one refuses and names what it found.
- integrity/nlc-version.json is not used to pick the milestone.

First checklist item (product owner, 2026-11-27 3:40 PM CT, unchanged):

> Do we have all the issues for this milestone competed? (this would be in the top of the checklist of the release, btw)

The first gate fails and names each open milestone issue.

## Readiness

Every ADR 0061 item is evaluated at entry. Every failing item is reported, then the goal stops. The same list is re-checked before validate, sign, main, and tag. Where an item cannot be checked before a later step produces its input (release notes and version-file align at validate, the tag at tag, the one release signature at sign), the gate output is `PENDING`, not `MET`.
