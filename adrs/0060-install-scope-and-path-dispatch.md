# ADR 0060 — Install scope (global or local) and PATH dispatch

- Status: Accepted
- Date: 2026-11-10
- Revision: 1
- Deciders: Human manager
- Ratified-by: Human manager (install into the current repo; PATH commands exec the repo copy, 2026-11-10)
- Class: E (boundary meaning of where the hub copy lives) + C (install use-case)
- Corpus: nlc
- Amends: [ADR 0015](0015-distribution-lock-and-version-store.md) (`store: project` layout and operator contract)
- Related: [ADR 0018](0018-human-cli-interview-on-gap.md) (gap copy), [ADR 0054](0054-published-skill-author-contract.md) (author check on the hub copied tree)
- Product story and reasons: [`docs/nlc/FEATURES.md`](../docs/nlc/FEATURES.md) item 2
- Version class of this change: **minor** (new operator requirement; PATH `nlc` in a locally pinned repo runs that copy)

## Context

[ADR 0015](0015-distribution-lock-and-version-store.md) named `store: project` on the lock file. Install still always wrote the user store (`~/.local/share/nlc`) and PATH `nlc` always ran that hub. A repo could not pin its own copy. Upgrading the machine-wide install dragged every repo along.

The operator contract for the pin is: the installer prompts **global** or **local**; any PATH shell command that **is** the global version, when a version exists in the current repo, calls that version and passes all the args.

## Decision

1. **Two install scopes.** `global` — user store, `~/.local/bin` shim, overlay hub skills into `~/.agents/skills`. `local` — hub bytes under `<repo>/.nlc` (`store: project`, `store_path: .nlc`), `./nlc` in that repo if missing, overlay hub skills into `<repo>/.agents/skills`. Local does not write the user-store hub or `~/.agents/skills`. Both scopes still install or refresh the PATH shim so dispatch works.

2. **How scope is chosen.** `--global` / `--local` or `NLC_INSTALL_SCOPE=global|local` win. If those are empty and stdout is a terminal and `CI` is unset, prompt on `/dev/tty` (or Windows host equivalent): global or local. Otherwise **global** (piped `curl | bash` and CI do not hang).

3. **Local needs a current repo.** Git worktree root walking from cwd. If none: refuse with problem + fix (cd into a repo, `git init`, or `--global`). Do not write a hub into an unrooted directory.

4. **PATH dispatch.** Identity of “the global version” is the installed path (`~/.local/bin/nlc` or `nlc.cmd`), not the script text. If this process is that shim, walk up from cwd. If `nlc` / `nlc.cmd` exists and is not this shim, `exec` it with unmodified argv. Else if `.nlc/lock.json` has `store: project` and that store’s `hub/tools/nlc.py` exists, exec that Python with `--project` the lock’s repo and the same argv. Failed exec is `NOT_MET`, not silent fall-back. The repo copy must not apply the PATH-shim check (no recursion). `NLC_HUB` does not skip this dispatch on the global shim.

5. **Skills.** Local overlay uses the same hub-only staging author check as global ([ADR 0054](0054-published-skill-author-contract.md)), then copies into the repo skills tree, not mixed home skills.

6. **Git.** The lock is the pin (committed). `.nlc/hub`, `.nlc/versions/`, and `.nlc/current` default gitignored. Vendoring those bytes is out of this record.

7. **Windows PATH command.** The file in `~/.local/bin/nlc.cmd` is the dispatching launcher (`scripts/nlc-launcher.cmd`), not the adopter `templates/adopter/nlc.cmd` (that file treats its own directory as `--project`).

## Consequences

- `python3 tools/nlc-init.py --store project` may write a project lock and copy the hub into the new app’s `.nlc`.
- `lock_validate` accepts `user` | `workspace` | `project` (schema already did). `workspace` remains unimplemented as an install prompt.
- Hub clone `./nlc` already is a repo version; PATH `nlc` inside that clone execs it.

## Rejected

- Hub as a git submodule inside the app repo (ADR 0015).
- Prompting on piped stdin (`read` would eat the script).
- Grading mixed destination skills after install.
- Letting `NLC_HUB` skip PATH dispatch when the binary is the global shim.
- Identity = “this file contains dispatch code” (a copied launcher in `./nlc` would loop).

## Proposal (G-PROPOSE)

- **Change class:** E + C
- **Nouns / verbs / goals touched:** distribution lock (`store`), `goals/hub_install`, PATH launchers, adopter `./nlc`
- **Adjectives that must hold:** piped install stays global without a prompt; local pin survives a later global upgrade; author check still runs on the hub copy
- **Non-goals:** workspace-root shared store; committing hub bytes; changing global overlay when the operator picked global
- **Tests:** `fitness-install-scope.py`; `assert-install-local-dispatch-passes.py`; `assert-install-local-outside-repo-fails.py`; `assert-install-foreign-skills-passes.py`
- **Impact:** PATH `nlc` in a locally pinned repo runs that hub; one-line install grows a TTY prompt
