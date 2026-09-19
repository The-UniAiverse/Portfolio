## What
<!-- one paragraph -->

## Checklist
- [ ] Branch follows `features/<name>` → `dev` → `main`
- [ ] `pytest -q` green locally
- [ ] Content change? `CHANGELOG.md` updated and `version` bumped in the YAML
- [ ] No secrets in the diff (.env, keys, tokens)
- [ ] For `main`: backup workflow ran (branch `backup/main-*` exists)
