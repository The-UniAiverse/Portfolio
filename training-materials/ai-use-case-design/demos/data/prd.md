# PRD — Shipment-status assistant
**Problem.** Agents spend 11 minutes per 'where is my shipment' email, 900 a week.
**Success metric.** Median handling time: baseline 11 min, target 5.5 min within 90 days.
**Users.** 12 customer-service agents in the pilot; the assistant drafts, the agent sends (human review of every reply).
**Data source.** TMS tracking API and 14 policy documents; access control by customer account.
**Evaluation set.** 120 real emails labelled by two senior agents.
**Out-of-scope.** Must not answer pricing, legal or HR questions; replies 'I could not find this' and routes to a person.
**Latency.** p95 under 6 seconds.
**Risk tier.** Limited (customer-facing, personal data in tracking records).
