# RCA — 2026-11-16-planit-identity-adopter-registry

## Verdict

**Result:** PASS (analysis completeness — not “fix applied”)

**Evidence:** At record time, `node metaprompts/scripts/validate-rca-record.mjs` (zyprompt) on this file → exit 0.

**The one thing:** ./nlc planit-identity is the only run of this check; it hashes the loaded planit SKILL.md against the hub registry and exits non-zero on mismatch

**Next:** Add that command on the hub CLI and point the Planit skill at it. Apply via a separate `/planit` or an explicit “apply this RCA”. This run does not edit the skill or the CLI.

---

## 1. Error condition

error_condition: In a new repo with a local install of Natural Language Compiler v0.7.0, Planit intake blocked because `integrity/planit-skill-registry.json` was absent at the product root. The file is present in the installed hub copy, and its hash matches the installed Planit skill. Nothing is supposed to create that file in the product repo.

Evidence (observed, 2026-11-16):

- Session: `bug.txt`. Repo: `upgrade-your-prompt` (a new product repo with a local v0.7.0 install). `.nlc/current` is `0.7.0`. `.nlc/hub` → `.nlc/versions/0.7.0`.
- The installed Planit skill (`.agents/skills/planit/SKILL.md` line 44) says, as a blocking intake check: run `python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md`, and names `integrity/planit-skill-registry.json` as the registry. The same sentence is in the v0.7.0 hub copy and in this repo’s `.agents/skills/planit/SKILL.md`.
- That command, from the product root, exited 2: `python3: can't open file 'upgrade-your-prompt/tools/fitness-planit-identity.py': [Errno 2] No such file or directory`.
- `ls integrity/planit-skill-registry.json` at the product root exited 2: `No such file or directory`. `CHARTER.md` at that root is an adopter stub, not the hub charter.
- The product root has no `tools/` directory. `is_hub_repo` on that root is false. `is_hub_repo` on `.nlc/versions/0.7.0` is true.
- The registry exists at `.nlc/versions/0.7.0/integrity/planit-skill-registry.json`. `content_sha256` is `4c395de82ca8f1a88d9f337b3675bc97d197243e12934116a9dd6e5e5a7e5b8c`, the same hash the session recorded for `.agents/skills/planit/SKILL.md`.
- Running the hub script from the product root (`python3 .nlc/hub/tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md`) printed `PLANIT_IDENTITY:MET` and exited 0. `resolve_root` in `tools/nouns/planit_identity/planit_identity.py` uses the script file’s hub (`Path(__file__).parents[3]`), not the product cwd. `--loaded .agents/skills/planit/SKILL.md` is then read inside that hub.
- `tools/nlc.py` in the v0.7.0 hub has no planit-identity command. `./nlc` already resolves `.nlc/hub` from `.nlc/lock.json` and execs `tools/nlc.py`.
- The writer is hub-only: `write_registry_from_bytes` in that same module, invoked by `tools/generate-planit-identity-registry.py`.

## 2. Impact / scope

Scope: this hub, and every adopter that installs it locally or globally and then runs `/planit`.

The v0.7.0 session stopped before the research plan. The agent told the operator to put the hub script and the registry into the product repo, or to waive the check. Copying the registry into the product repo would not make that repo a hub, and the checker skips non-hub trees (`PLANIT_IDENTITY:MET skip (hub-only gate, not hub tree)`).

Severity: moderate. One adopter session blocked. Not a shipped-tag outage. The same skill sentence is still in this repo, so the next install will do it again until the skill and the CLI change.

## 3. Timeline

1. Local install of v0.7.0 pinned the hub under `.nlc/versions/0.7.0` and copied Planit into `.agents/skills/planit/SKILL.md` unchanged.
2. `/planit` followed the skill’s identity sentence and ran `python3 tools/fitness-planit-identity.py` in the product repo.
3. The script is not at that path. The agent then looked for `integrity/planit-skill-registry.json` at the product root, because the same sentence names that relative path.
4. Intake verdict was BLOCKED. The operator asked what should create the registry.
5. The agent searched GitHub `main` instead of `.nlc/hub`, where both the file and `tools/generate-planit-identity-registry.py` already were.

## 4. The one thing

one_thing: ./nlc planit-identity is the only run of this check; it hashes the loaded planit SKILL.md against the hub registry and exits non-zero on mismatch

The skill sentence is the invocation. Install, bare `./nlc`, and opening the skill do not run the check. If `./nlc planit-identity` is not executed, the check is not executed.

The command is the check, not a pointer at the existing script. It takes the Planit file the agent loaded, hashes those bytes, and compares them to `integrity/planit-skill-registry.json` in the hub `./nlc` already resolves (`.nlc/hub` for a local pin, otherwise the user store). Mismatch or a missing hub registry exits non-zero. It does not read `integrity/` in the product repo, and it does not skip the comparison because the product repo is not a hub.

The current checker does not do that. `prove()` in `tools/nouns/planit_identity/planit_identity.py` reads `--loaded` relative to the hub that contains the script, and it rejects a path that is not the canonical relative string. A non-hub root skips. So the MET result in §1 hashed the hub’s own skill, not the product-repo file the agent loaded.

## 4b. System layer classification

| Layer | Implicated? | Evidence | Recommended control (summary) |
| ----- | ----------- | -------- | ----------------------------- |
| L0 Symptom | N | The product root is not a hub. Absence of `integrity/planit-skill-registry.json` there is the install layout. The hub copy exists and matches the skill hash. | none — do not create the file in the adopter |
| L1 Local system | Y | `./nlc` resolves the hub, then execs `tools/nlc.py`. That CLI has no identity subcommand. The existing checker hashes the hub’s own skill or skips a non-hub root. It never hashes the loaded product-repo skill against the hub registry. | `./nlc planit-identity` hashes the loaded skill file against the hub registry and exits non-zero on mismatch. It does not skip an adopter. |
| L2 Meta-system | Y | `.agents/skills/planit/SKILL.md` line 44 is the only invocation, and it names a cwd-relative script and registry that a local install does not place at the product root. | That sentence calls `./nlc planit-identity` on the loaded skill file. If that command is not run, the check is not executed. |

## 5. Prevention test

If the skill’s only identity invocation were `./nlc planit-identity` on the loaded skill file, and that command hashed those bytes against the hub registry, the product-root `ls` of `integrity/planit-skill-registry.json` would not be the check. A missing hub registry or a hash mismatch would still exit non-zero. Skipping the command would mean the check did not run.

```
prevention_test:
cmd: pytest tools/test_planit_identity_adopter.py -q
```

The test does not exist yet. The apply run adds it. It must exit non-zero if `.agents/skills/planit/SKILL.md` still contains `python3 tools/fitness-planit-identity.py`, and it must exit non-zero if `./nlc planit-identity` in a fixture adopter looks for `integrity/planit-skill-registry.json` at the adopter root.

## 6. Poke-yoke (mandatory — apex)

| Field | Value |
|-------|-------|
| poke_yoke | The identity check runs only as `./nlc planit-identity` on the loaded Planit file. That command hashes those bytes against `integrity/planit-skill-registry.json` in the resolved hub. Mismatch or a missing hub registry exits non-zero and blocks intake. It does not consult the product-repo `integrity/` directory and does not skip because the product repo is not a hub. No other entry point runs the check. |
| on_trip | `remediate:hub` — from the hub path printed by ./nlc planit-identity, run python3 tools/generate-planit-identity-registry.py, then re-run ./nlc planit-identity. Do not create integrity/planit-skill-registry.json in the adopter. |
| guarantee | After this control is applied, the check runs only when `./nlc planit-identity` is executed, and that execution compares the loaded skill bytes to the hub registry. A product-root registry is not an input. A mismatch or a missing hub registry cannot pass. |

## 7. Contributing factors

- The agent treated the skill’s relative path as an adopter path, then searched GitHub `main` instead of `.nlc/hub`. That slowed the session. The skill sentence is what made the missing product-root file look like a defect.
- `resolve_root` keys off the script file, not the process cwd. Once the hub script is the one invoked, `--loaded .agents/skills/planit/SKILL.md` is read inside the hub. The MET result above does not mean the checker inspected the adopter file as a separate tree.

## 8. Recommended preventive actions

status: recommended

### 8.1 Meta-system (L2)

| Field | Value |
|-------|-------|
| layer | L2 |
| status | recommended |
| Owner | Planit skill |
| Path / artifact | `.agents/skills/planit/SKILL.md` identity paragraph (installed copy follows this file) |
| poke_yoke | The identity sentence’s only command is `./nlc planit-identity` with the loaded skill path. That call is the invocation. Intake stays blocked when the command exits non-zero. The sentence does not name `tools/fitness-planit-identity.py` or a product-root `integrity/planit-skill-registry.json`. |
| on_trip | `remediate:hub` — if `./nlc planit-identity` exits non-zero, run `python3 tools/generate-planit-identity-registry.py` in the hub path the command prints, then re-run `./nlc planit-identity`. Do not add the registry to the adopter. |
| guarantee | An agent that follows the skill cannot be sent to create `integrity/planit-skill-registry.json` in a product repo, because the skill no longer names that path. |
| Verification command | `cmd: pytest tools/test_planit_identity_adopter.py::test_skill_identity_command -q` |
| Apply via | separate `/planit` / explicit apply — **not** `/conduct-rca` |

### 8.2 Local system (L1)

| Field | Value |
|-------|-------|
| layer | L1 |
| status | recommended |
| Owner | hub CLI |
| Path / artifact | `tools/nlc.py` subcommand `planit-identity`, using the hub already resolved by `./nlc` (`.nlc/hub` for a local pin, user store otherwise) |
| poke_yoke | `planit-identity` hashes the file passed as the loaded skill against `integrity/planit-skill-registry.json` in the hub `./nlc` resolved. Mismatch or a missing hub registry exits non-zero. An adopter root is not a skip and is not the registry location. The existing `prove()` hub-relative read is not this check. |
| on_trip | `remediate:hub` — run `python3 tools/generate-planit-identity-registry.py` in the hub directory named in the non-zero output, then `./nlc planit-identity`. |
| guarantee | Executing `./nlc planit-identity` on the loaded skill cannot pass when those bytes differ from the hub registry, and it cannot require a registry at the product root. If the command is not executed, this check has not run. |
| Verification command | `cmd: pytest tools/test_planit_identity_adopter.py::test_nlc_planit_identity_skips_adopter -q` |
| Apply via | separate `/planit` / explicit apply — **not** `/conduct-rca` |

## 9. Follow-up

Detection only, after the poke-yoke above. Not a substitute.

- v0.7.0 installs keep the old skill sentence until a hub that contains the new command is installed. The apply run does not rewrite already-pinned `.nlc/versions/0.7.0` trees.
- Do not add an adopter-root copy of the registry as a workaround. The checker’s non-hub result is a skip, not a missing file.
