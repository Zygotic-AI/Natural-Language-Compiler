# Hub release

The hub release is seven steps, one command each ([ADR 0061](../../adrs/0061-release-in-seven-steps.md)). Nothing else runs in a release.

| # | Step | Command | Who |
| --- | --- | --- | --- |
| 1 | main to release branch | `gh workflow run start-release.yml -f version=vX.Y.Z` | agent |
| 2 | change branch cut from `release/vX.Y.Z`, merged back, one at a time | `gh pr merge <PR> --merge` | agent |
| 3 | validate | `./release validate` | agent |
| 4 | sign, once, after validate | `./release sign` | owner |
| 5 | release to main | `./release main` | agent |
| 6 | tag main | `./release tag` | agent |
| 7 | artifacts from the tag trigger | [`.github/workflows/release.yml`](../../.github/workflows/release.yml) | CI |

## What the commands do

- `./release validate`, on `release/vX.Y.Z`: in a fresh worktree of `origin/release/vX.Y.Z` it writes `integrity/nlc-version.json` and the noop migration, rewrites `docs/adoption/RELEASE-vX.Y.Z.md` from the titles of PRs merged since the previous tag (step 2's `--merge` keeps each title in its merge commit) and checks it, regenerates derived files, commits, then runs `./nlc gate --profile release`. Green: pushes and prints `RELEASE_VALIDATE:ONLY_SIGNATURE_LEFT` and the statement (also on a branch already validated). Red: prints `RELEASE_VALIDATE:CODE_DEFECT` and pushes nothing; fix it in a change branch and run validate again.
- `./release sign` (owner key): on a clean `release/vX.Y.Z` whose HEAD is `origin/release/vX.Y.Z`, it reruns validate's writes on HEAD (they must change nothing) and the release suite (it must pass), then clearsigns the statement into `integrity/checker-digest.sha256.approval.asc`, commits, pushes.
- `./release main`: pushes `origin/release/vX.Y.Z` to `main` only if its tree, without the armor file, is the signed `Tree` (read from the statement gpg verifies with the previous release tag's keys; that tag is the nearest release tag on the first-parent line, v0.8.0 or a tag whose own statement verifies). Git refuses if `main` moved.
- `./release tag`: tags `origin/main` with the version in `integrity/nlc-version.json` only if its tree, without the armor file, is the signed `Tree` and the previous release tag's checker, with that tag's owner keys, returns MET.
- `release.yml` stops before building unless the tag is `v` plus the version in `integrity/nlc-version.json`.
- Validate and sign refuse a dirty worktree or local commits `origin` does not have.
- Bare `./release` prints the commands and exits 1.

Release notes format: [`.agents/instructions/release-notes.md`](../../.agents/instructions/release-notes.md).
