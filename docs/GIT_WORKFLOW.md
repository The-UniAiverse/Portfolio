# Git workflow (standard for all uniAIverse repos)

```
features/sarfi ─┐
features/harsh ─┼─► dev ─► main ─► deploy (api.uniaiverse.ai)
features/sahil ─┘        ▲
                 backup/main-<date> + tag created automatically before every merge to main
```

1. Work on your own branch: `features/<name>` (long-lived) or `features/<name>/<topic>` (short-lived).
2. Open a PR into `dev`. CI must be green. One other owner reviews.
3. `dev` → `main` PR once a week (or per release). The `backup-before-merge` workflow snapshots `main` first.
4. Merge to `main` deploys automatically.
5. Hotfix: branch from `main` as `hotfix/<topic>`, PR to `main`, then merge `main` back into `dev`.

Rollback: `git checkout backup/main-<date>` → PR to main, or `git revert` the merge commit.

## First-time setup for this repo
```bash
git remote add origin git@github.com:The-UniAiverse/ai-services.git
git checkout -b main && git push -u origin main
git checkout -b dev && git push -u origin dev
git checkout -b features/sarfi && git push -u origin features/sarfi
```
Then in GitHub → Settings → Branches: protect `main` and `dev` (require PR + CI).
Secrets for Actions: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_KEY`, `API_URL`, `ADMIN_TOKEN`.
