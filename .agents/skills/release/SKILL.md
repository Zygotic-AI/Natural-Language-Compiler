---
name: release
description: Hub release in seven steps (ADR 0061). Use when the user wants to release, ship, tag, or run ./release.
disable-model-invocation: true
---

# Release (`/release`)

The hub release is seven steps, one command each (ADR 0061). Run them in order. Nothing else runs in a release.

1. `gh workflow run start-release.yml -f version=vX.Y.Z` (on the owner's go).
2. `gh pr merge <PR> --merge` for one change branch cut from `release/vX.Y.Z`; cut the next one after it merges.
3. `./release validate` on `release/vX.Y.Z`. On `RELEASE_VALIDATE:CODE_DEFECT`, fix the named check in a change branch (step 2) and run it again.
4. Give the owner only the text between the `RELEASE_SIGN_BLOCK` markers, never commands. The owner returns a clearsigned message. Save it to a file and run `./release sign --armor <file>` (it re-proves validate on HEAD, then takes that file). Never create armor.
5. `./release main`.
6. `./release tag`.
7. The tag push runs `.github/workflows/release.yml`, which builds and publishes. Report the Release link.

Mandated pins: when a change touches a mandated path (`python3 tools/derive-mandated-paths.py`), `./release validate` regenerates the pins.

If a command's output contradicts the docs, fix the tool or the docs; never tell the owner to ignore or reinterpret it (`jidoka-ssot-output.md`).

Do not move an existing tag, reset `main`, or force-push. Do not write `Released-by:` (adopter ship, [`references/release-vs-product.md`](references/release-vs-product.md)).
