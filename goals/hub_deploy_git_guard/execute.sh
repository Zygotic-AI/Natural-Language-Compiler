#!/usr/bin/env bash
# Refuse deploy/release unless HEAD is origin/main tip (branch deploy) or
# DEPLOY_GIT_REF resolves to a commit that is an ancestor of origin/main (tag deploy).
# No override: non-zero exit only.
set -euo pipefail

REMOTE="${DEPLOY_GIT_REMOTE:-origin}"
BASE="${DEPLOY_GIT_BASE:-main}"
REF="${DEPLOY_GIT_REF:-}"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "deploy_git_guard: refuse — not a git repository"
  exit 1
fi

if ! git remote get-url "${REMOTE}" >/dev/null 2>&1; then
  echo "deploy_git_guard: refuse — remote ${REMOTE} is not configured"
  exit 1
fi

git fetch "${REMOTE}" "${BASE}" --quiet

main_ref="${REMOTE}/${BASE}"
if ! git rev-parse --verify --quiet "${main_ref}" >/dev/null; then
  echo "deploy_git_guard: refuse — ${main_ref} does not exist"
  exit 1
fi

main_sha="$(git rev-parse "${main_ref}")"

if [[ -n "${REF}" ]]; then
  if ! commit_sha="$(git rev-parse --verify "${REF}^{commit}" 2>/dev/null)"; then
    echo "deploy_git_guard: refuse — cannot resolve DEPLOY_GIT_REF=${REF}"
    exit 1
  fi
  if ! git merge-base --is-ancestor "${commit_sha}" "${main_ref}"; then
    echo "deploy_git_guard: refuse — ${REF} (${commit_sha}) is not contained in ${main_ref} (${main_sha})"
    exit 1
  fi
  echo "deploy_git_guard: MET tag ${REF} (${commit_sha}) on ${main_ref}"
  exit 0
fi

head_sha="$(git rev-parse HEAD)"
if [[ "${head_sha}" != "${main_sha}" ]]; then
  echo "deploy_git_guard: refuse — HEAD (${head_sha}) is not ${main_ref} tip (${main_sha}); merge origin/main or deploy only from main"
  exit 1
fi

echo "deploy_git_guard: MET HEAD is ${main_ref} tip (${main_sha})"
exit 0
