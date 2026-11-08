# Vendored third-party code

## ai-job-search

- Upstream: https://github.com/ai-job-search-dev/ai-job-search (MIT, Copyright (c) 2026 Mads Lorentzen; see `ai-job-search/LICENSE`)
- Vendored commit: `e16acee3abdaae57f8026789338a3c6eebf4608b`
- Kept **unmodified** so upstream updates can be pulled in. Do not edit files under `ai-job-search/`;
  adapt behaviour in `app/services/jobs/` instead.

What the platform uses from it (see `app/services/jobs/upstream.py`):

| Upstream piece | Used for |
|---|---|
| `.agents/skills/freehire-search/cli` (Bun) | Job search and job detail (`/api/jobs/search`, `/api/jobs/job/{slug}`) |
| `tools/posting_guard.py` | Cleans every posting and flags hidden or injected text before it reaches the AI model |
| `tools/rank_state.py` (`WEIGHTS`, `BANDS`, `overall_score`, `band`) | Combines the per-dimension fit scores |
| `.claude/skills/job-application-assistant/04-job-evaluation.md` | Fit-scoring rubric given to the AI model |
| `.claude/commands/rank.md` | The scoring JSON contract |
| `.claude/skills/job-application-assistant/03-writing-style.md`, `06-cover-letter-templates.md` | Cover-letter drafting rules |
| `.claude/agents/application-reviewer.md` | Grounding rules for the cover-letter review pass |
| `cover_letters/OpenFonts/fonts/lato` | Fonts for the cover-letter PDF |

Not used: the Claude Code commands themselves (`/setup`, `/apply`, …), LaTeX compilation, the LinkedIn
connector (LinkedIn's terms forbid automated commercial use) and the Danish job portals.

Runtime requirement: [Bun](https://bun.sh) on `PATH` (or `BUN_BIN`) for the job connector.

### Updating

```bash
git clone https://github.com/ai-job-search-dev/ai-job-search /tmp/ai-job-search
rsync -a --delete --exclude .git --exclude node_modules /tmp/ai-job-search/ apps/api/vendor/ai-job-search/
cd apps/api && pytest -q      # the jobs tests pin the upstream interfaces we call
```
Then update the commit hash above.
