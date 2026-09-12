# AI Engineer — Course Plan (8 × 4h)
**Audience:** developers / data engineers with Python. **Promise:** ship one ML or AI feature end-to-end with an API, tests and monitoring.

| Day | Theme | Lab |
|---|---|---|
| 1 | Problem framing & data: from business ask to ML task; data audit; leakage; baselines | Frame a real use case, write the eval metric before any model |
| 2 | Data pipelines: ingestion, validation (Great Expectations / pandera), feature tables, versioning | Build a validated pipeline with a data-quality report |
| 3 | Classical ML that still wins: gradient boosting, calibration, explainability (SHAP) | Train/evaluate a tabular model; produce a model card |
| 4 | Working with LLM APIs: structured output, tool calling, batching, rate limits, retries | Wrap an LLM behind a typed service with tests |
| 5 | Serving: FastAPI, containers, config-driven design, secrets, CI | Dockerise + CI the service from day 4 |
| 6 | MLOps: experiment tracking (MLflow), model registry, blue/green, rollback | Register two versions, switch traffic, roll back |
| 7 | Monitoring: data drift, prediction drift, latency/cost dashboards, alerting | Add drift detection and an alert to the deployed service |
| 8 | Capstone: end-to-end feature, reviewed against the Definition of Done | Demo + review |

**Definition of Done for the capstone:** eval set in repo · reproducible training/inference · API with schema validation · CI passing · monitoring and rollback path documented.
