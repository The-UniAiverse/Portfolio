#!/usr/bin/env bash
# Safe push: checks first, then commits and pushes YOUR branch. Never pushes to main or dev directly.
#   ./scripts/push_to_github.sh "what I changed"                 (uses the current branch; must start with features/)
#   ./scripts/push_to_github.sh "what I changed" --fast           (skips running every course demo; CI still runs them)
# First time only:  git remote add origin git@github.com:The-UniAiverse/ai-services.git
set -euo pipefail
MSG="${1:?Give a short message in quotes, e.g. \"content: new bot answer about refunds\"}"; FAST="${2:-}"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
case "$BRANCH" in features/*) ;; *) echo "You are on '$BRANCH'. Work on your own branch:  git checkout features/sarfi"; exit 1;; esac
git remote get-url origin >/dev/null 2>&1 || { echo "No GitHub remote yet. Run once:  git remote add origin git@github.com:The-UniAiverse/ai-services.git"; exit 1; }
if git ls-files --error-unmatch .env >/dev/null 2>&1; then echo ".env is tracked by git — it holds secrets. Run:  git rm --cached .env"; exit 1; fi
echo "1/4 rebuilding course kits";  python scripts/build_course_kits.py >/dev/null
echo "2/4 checking content";        if [ "$FAST" = "--fast" ]; then python scripts/validate_content.py --no-demos; else python scripts/validate_content.py; fi
echo "3/4 running engine tests";    python -m pytest -q
echo "4/4 committing and pushing";  git add -A; git commit -qm "$MSG" || echo "(nothing new to commit)"; git push -u origin "$BRANCH"
echo; echo "Pushed $BRANCH. Next: open a pull request  $BRANCH → dev  on GitHub. CI must be green before merging."
