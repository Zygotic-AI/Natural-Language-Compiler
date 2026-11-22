# nlc_release_tag_gate

ADR 0061 steps 3 to 6 behind `./release validate|sign|main|tag` (`scripts/nlc-release.sh` only dispatches), plus the notes and statement validate writes.

The trust root for steps 5 and 6 is the nearest release tag on the first-parent line: `ANCHOR` (v0.8.0), or a tag whose own commit carries a statement its previous tag verifies with a matching Tree. Tags on side commits are never used.
