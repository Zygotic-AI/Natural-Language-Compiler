#!/usr/bin/env bash
# Natural Language Compiler — install portable skills into the user's agent harness.
# macOS, Linux, WSL. Requires: bash, curl or git, mkdir, cp or rsync.
# Scope: global (user store) or local (current repo). ADR 0060.
set -euo pipefail

# ADR 0013 — requirements preflight (all gaps, then exit)
requirements_preflight() {
  local -a missing=()
  command -v python3 >/dev/null 2>&1 || missing+=("python3")
  local script_dir local_marker
  script_dir="$(cd "$(dirname "$0")" && pwd)"
  local_marker="${script_dir}/../../.agents/skills/planit/SKILL.md"
  if [[ ! -f "${local_marker}" ]]; then
    command -v curl >/dev/null 2>&1 || missing+=("curl")
  fi
  if ((${#missing[@]} > 0)); then
    echo "Install can't continue — this machine is missing required tools." >&2
    local m
    for m in "${missing[@]}"; do
      echo "  What's wrong: missing ${m}" >&2
    done
    echo "  Fix: install the tools above, or clone this repo and run: bash scripts/install.sh" >&2
    exit 1
  fi
}
requirements_preflight

SCOPE="${NLC_INSTALL_SCOPE:-}"
for arg in "$@"; do
  case "$arg" in
    --global) SCOPE=global ;;
    --local) SCOPE=local ;;
  esac
done
SCOPE="$(printf '%s' "${SCOPE}" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')"
if [[ -z "${SCOPE}" ]]; then
  if [[ -z "${CI:-}" && -t 1 ]]; then
    echo "Install where?"
    echo "  global — this user (~/.local/share/nlc, ~/.agents/skills)"
    echo "  local  — this repo (.nlc/hub, ./nlc)"
    printf "global or local [global]: "
    if [[ -r /dev/tty ]]; then
      read -r SCOPE < /dev/tty || SCOPE=global
    else
      SCOPE=global
    fi
  fi
  SCOPE="$(printf '%s' "${SCOPE:-global}" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')"
fi
if [[ "${SCOPE}" != "global" && "${SCOPE}" != "local" ]]; then
  echo "Install can't continue — install place must be global or local." >&2
  echo "  What's wrong: got ${SCOPE:-empty}" >&2
  echo "  Fix: pass --global or --local, or set NLC_INSTALL_SCOPE." >&2
  echo "INSTALL:NOT_MET invalid install scope" >&2
  exit 1
fi

NLC_REPO_SLUG="${NLC_REPO_SLUG:-Zygotic-AI/Natural-Language-Compiler}"
NLC_RAW_BASE="${NLC_RAW_BASE:-https://raw.githubusercontent.com/${NLC_REPO_SLUG}/main}"
NLC_REF="${NLC_REF:-}"
REPO_ROOT=""
if [[ "${SCOPE}" == "local" ]]; then
  if ! command -v git >/dev/null 2>&1; then
    echo "Install can't continue — local install needs git to find the current repo." >&2
    echo "  What's wrong: missing git" >&2
    echo "  Fix: install git, or pass --global." >&2
    echo "INSTALL:NOT_MET local install needs git" >&2
    exit 1
  fi
  REPO_ROOT="$(git -C "${PWD}" rev-parse --show-toplevel 2>/dev/null || true)"
  if [[ -z "${REPO_ROOT}" || ! -d "${REPO_ROOT}" ]]; then
    echo "Install can't continue — local install needs a git repo." >&2
    echo "  What's wrong: ${PWD} is not inside a git worktree" >&2
    echo "  Fix: cd into the repo, run git init, or pass --global." >&2
    echo "INSTALL:NOT_MET local install without a repo" >&2
    exit 1
  fi
  INSTALL_ROOT="${REPO_ROOT}/.nlc"
  AGENTS_SKILLS="${REPO_ROOT}/.agents/skills"
  CURSOR_SKILLS="${REPO_ROOT}/.cursor/skills"
  CURSOR_HOME="${REPO_ROOT}/.cursor"
else
  INSTALL_ROOT="${NLC_INSTALL_ROOT:-${HOME}/.local/share/nlc}"
  AGENTS_SKILLS="${HOME}/.agents/skills"
  CURSOR_SKILLS="${HOME}/.cursor/skills"
  CURSOR_HOME="${HOME}/.cursor"
fi

tmpdir=""
cleanup() {
  if [[ -n "${tmpdir}" && -d "${tmpdir}" ]]; then
    rm -rf "${tmpdir}"
  fi
}
trap cleanup EXIT

echo "Natural Language Compiler — install"
echo "  scope: ${SCOPE}"
echo "  target: ${INSTALL_ROOT}"
echo "  skills: ${AGENTS_SKILLS}"

mkdir -p "${INSTALL_ROOT}" "${AGENTS_SKILLS}"

script_dir="$(cd "$(dirname "$0")" && pwd)"
if [[ -f "${script_dir}/../../.agents/skills/planit/SKILL.md" ]]; then
  src_root="$(cd "${script_dir}/../.." && pwd)"
  echo "  source: local repo ${src_root}"
  python3 "${src_root}/tools/nlc-fetch-hub.py" --install-root "${INSTALL_ROOT}" --from-path "${src_root}"
  src_root="${INSTALL_ROOT}/hub"
else
  tmpdir="$(mktemp -d)"
  tool_dir="${tmpdir}/nlc-tools"
  mkdir -p "${tool_dir}"
  curl -fsSL "${NLC_RAW_BASE}/tools/nlc-fetch-hub.py" -o "${tool_dir}/nlc-fetch-hub.py"
  curl -fsSL "${NLC_RAW_BASE}/tools/nlc_distribution.py" -o "${tool_dir}/nlc_distribution.py"
  curl -fsSL "${NLC_RAW_BASE}/tools/nlc_requirements.py" -o "${tool_dir}/nlc_requirements.py"
  fetch_args=(--install-root "${INSTALL_ROOT}" --repo "${NLC_REPO_SLUG}")
  if [[ -n "${NLC_VERSION:-}" ]]; then
    fetch_args+=(--version "${NLC_VERSION}")
  elif [[ -n "${NLC_REF}" ]]; then
    fetch_args+=(--version "${NLC_REF#v}")
  fi
  echo "  source: release tarball (latest semver unless NLC_VERSION/NLC_REF set)"
  python3 "${tool_dir}/nlc-fetch-hub.py" "${fetch_args[@]}"
  src_root="${INSTALL_ROOT}/hub"
fi

skills_src="${src_root}/.agents/skills"
if [[ ! -d "${skills_src}" ]]; then
  echo "Install could not find published skills in the hub copy." >&2
  echo "  What's wrong: missing ${skills_src}" >&2
  echo "  Fix: re-run install from a hub that includes .agents/skills." >&2
  echo "INSTALL:NOT_MET missing hub skills" >&2
  exit 1
fi

# ADR 0054: same CLI on the copied hub skills tree, not mixed destination skills.
if [[ -z "${tmpdir}" ]]; then
  tmpdir="$(mktemp -d)"
fi
skills_staging="${tmpdir}/hub-skills"
mkdir -p "${skills_staging}"
if command -v rsync >/dev/null 2>&1; then
  rsync -a "${skills_src}/" "${skills_staging}/"
else
  cp -R "${skills_src}/." "${skills_staging}/"
fi

skill_check_goal="${INSTALL_ROOT}/hub/goals/hub_skill_author_check/execute.sh"
if [[ ! -f "${skill_check_goal}" ]]; then
  echo "Install could not confirm installed skills are authored correctly." >&2
  echo "  What's wrong: missing goals/hub_skill_author_check/execute.sh" >&2
  echo "  Fix: re-run install from a hub that includes the skill-author use-case." >&2
  echo "INSTALL:NOT_MET missing skill author check" >&2
  exit 1
fi
echo "  verify: skill author checklist"
bash "${skill_check_goal}" --root "${skills_staging}" || {
  echo "Install could not confirm the hub skills copy is authored correctly." >&2
  echo "  What's wrong: published skill checklist failed on the hub skills copy (not other skills already in ${AGENTS_SKILLS})" >&2
  echo "  Fix: repair the hub skills, then re-run install." >&2
  echo "INSTALL:NOT_MET skill author checklist failed" >&2
  exit 1
}

if command -v rsync >/dev/null 2>&1; then
  rsync -a "${skills_staging}/" "${AGENTS_SKILLS}/"
else
  cp -R "${skills_staging}/." "${AGENTS_SKILLS}/"
fi

if [[ -d "${CURSOR_HOME}" ]]; then
  mkdir -p "${CURSOR_SKILLS}"
  for skill in bbp-confirmer bbp-proposer bbp-recorder bbp-reviewer interview planit verify; do
    if [[ -d "${src_root}/.cursor/skills/${skill}" ]]; then
      rm -rf "${CURSOR_SKILLS}/${skill}"
      cp -R "${src_root}/.cursor/skills/${skill}" "${CURSOR_SKILLS}/${skill}"
    fi
  done
  echo "  cursor: copied repo-local BBP + planit skills"
fi

if [[ -z "${NLC_SKIP_VERIFY:-}" ]] && [[ -f "${INSTALL_ROOT}/hub/tools/nlc-install-verify.py" ]]; then
  echo "  verify: hub file hashes"
  python3 "${INSTALL_ROOT}/hub/tools/nlc-install-verify.py" "${INSTALL_ROOT}/hub" || {
    echo "Install could not verify the compiler file fingerprints." >&2
    echo "  What's wrong: hub files do not match published fingerprints" >&2
    echo "  Fix: re-run install from a clean checkout, or repair the hub tree." >&2
    echo "  Optional: NLC_SKIP_VERIFY=1 only if you accept running an unverified hub." >&2
    echo "INSTALL:NOT_MET hub verify failed" >&2
    exit 1
  }
fi

if [[ -f "${INSTALL_ROOT}/current" ]]; then
  echo "  hub version: $(tr -d '\n' < "${INSTALL_ROOT}/current")"
fi

if [[ "${SCOPE}" == "local" ]]; then
  python3 - "${REPO_ROOT}" "${src_root}" <<'PY'
import sys
from pathlib import Path

repo = Path(sys.argv[1])
hub = Path(sys.argv[2])
sys.path.insert(0, str(hub / "tools"))
from nlc_distribution import read_hub_version, write_project_lock

write_project_lock(
    repo,
    hub_version=read_hub_version(hub),
    store="project",
    store_path=".nlc",
)
gi = repo / ".gitignore"
extra = [".nlc/hub", ".nlc/versions/", ".nlc/current"]
existing = gi.read_text(encoding="utf-8") if gi.is_file() else ""
add = [line for line in extra if line not in existing.splitlines()]
if add:
    prefix = "" if not existing or existing.endswith("\n") else "\n"
    gi.write_text(existing + prefix + "\n".join(add) + "\n", encoding="utf-8")
PY
  if [[ ! -e "${REPO_ROOT}/nlc" ]]; then
    if [[ -f "${src_root}/templates/adopter/nlc" ]]; then
      cp "${src_root}/templates/adopter/nlc" "${REPO_ROOT}/nlc"
      chmod +x "${REPO_ROOT}/nlc"
      echo "  command: ${REPO_ROOT}/nlc"
    fi
  fi
  if [[ ! -e "${REPO_ROOT}/nlc.cmd" && -f "${src_root}/templates/adopter/nlc.cmd" ]]; then
    cp "${src_root}/templates/adopter/nlc.cmd" "${REPO_ROOT}/nlc.cmd"
  fi
fi

BIN_DIR="${HOME}/.local/bin"
mkdir -p "${BIN_DIR}"
launcher="${INSTALL_ROOT}/hub/scripts/nlc-launcher.sh"
if [[ -f "${launcher}" ]]; then
  cp "${launcher}" "${BIN_DIR}/nlc"
  chmod +x "${BIN_DIR}/nlc"
  echo "  path command: ${BIN_DIR}/nlc (add ~/.local/bin to PATH if needed)"
fi
win_launcher="${INSTALL_ROOT}/hub/scripts/nlc-launcher.cmd"
if [[ -f "${win_launcher}" ]]; then
  cp "${win_launcher}" "${BIN_DIR}/nlc.cmd"
fi

cat <<EOF

Done.

Scope: ${SCOPE}
Hub copy (tools, charter): ${INSTALL_ROOT}/hub
Portable skills: ${AGENTS_SKILLS}

Next:
  Run: nlc   (human menu — see ${INSTALL_ROOT}/hub/docs/nlc/MENU.md)

  Or in Cursor: /interview then /planit

EOF
