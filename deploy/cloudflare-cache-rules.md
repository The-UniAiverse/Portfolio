# Cloudflare rules for api.uniaiverse.ai
Cache (Edge TTL 1 hour, respect origin): `/static/*`, `/api/readiness_audit/questionnaire*`, `/api/readiness_audit/framework`, `/api/readiness_audit/tiers`, `/api/training/curriculum`, `/api/training/tracks`, `/api/quest/tiers`, `/api/pricing/*`, `/api/demos`, `/api/discovery/kit`
Bypass cache: everything under `/api/*` not listed (POSTs, per-user progress, payments, admin).
Rate limit: `/api/demos/run/*` 30 requests / minute / IP; `/api/quest/quiz*` 60 / minute / IP; `/api/payments/*` 20 / minute / IP.
WAF: managed ruleset on; block countries only if abuse appears.
