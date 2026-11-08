# Hub in-force surface exclusions (O6)

Gates **fitness-hub-public-self-contained** and **fitness-internal-links** treat every file under the repo as **in-force** unless its path matches an exclusion below. This is an exclusion list only; history and RCA instance records stay out of scope.

## Excluded prefixes

| Prefix | Reason |
|--------|--------|
| `docs/history/` | Archived prose; not operating law |
| `adrs/history/` | Previous ADR bytes; not current law (ADR 0059) |
| `docs/rca/` | RCA instance records (may cite old paths and names) |
| `theory/history/` | Frozen theory drafts |
| `examples/` | Adopter fixtures and landmines |
| `node_modules/`, `.git/`, `.venv/`, `venv/`, `__pycache__/` | Tooling caches |

## Excluded top-level names

| Name | Reason |
|------|------|
| `uploads/` | Ephemeral agent uploads |

## Person-name gate (CG-R4)

CG-R4 refuses **person-as-actor** language on process and decision SSOT (use cases, instructions, ADR Deciders, role SOPs, and similar): name the role, not the person who happens to hold it. It does **not** forbid a dedicated contributor-attribution page.

Person-name patterns apply to every tracked repo text file (`.md`, `.mdc`, `.json`, `.txt`, `.yaml`, `.yml`) **except** the paths below. Forbidden private-repo markers still use the in-force exclusions above.

### Person-name scan exclusions

| Path | Reason |
|------|--------|
| `CONTRIBUTORS.md` | Attribution surface: who holds an area (portrait / profile / display name). Not process-actor prose. |

Implementation: `tools/nouns/hub_in_force_surfaces/hub_in_force_surfaces.py` (`EXCLUDED_PREFIXES`, `EXCLUDED_TOP_LEVEL`, `PERSON_NAME_EXCLUDED_RELS`).
