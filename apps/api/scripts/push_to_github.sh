#!/usr/bin/env bash
# Usage: ./scripts/push_to_github.sh <git-remote-url> [branch]
# Example: ./scripts/push_to_github.sh git@github.com:waghmarepb/uniaiverse-ai-services.git sarfi/dev
set -euo pipefail
# Legacy: written for the standalone backend repo. Inside the uniAIverse monorepo it would
# replace `origin` and commit the whole repository, so refuse to run there.
if [ -d "$(git rev-parse --show-toplevel 2>/dev/null)/apps/api" ]; then
  echo "Refusing to run inside the monorepo; push with normal git commands from the repo root." >&2
  exit 1
fi
REMOTE="${1:?remote url required}"; BRANCH="${2:-sarfi/dev}"
git init -q 2>/dev/null || true
git checkout -B "$BRANCH"
git add -A
git commit -qm "feat: AI services API — readiness audit (P1), training catalogue (P2), strategy/governance/automation (P3-P4), pricing tiers" || true
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE"
git push -u origin "$BRANCH"
echo "Pushed $BRANCH → $REMOTE"
