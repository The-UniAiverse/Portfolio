"""AI Engineer · Demo 5 — Serving: a config-driven prediction API with health, secrets hygiene and CI checks (25 min) · Module 5
Shows: a FastAPI prediction service started in-process: config from environment, /health and /predict with input validation, a secrets scan and the CI checklist that gates a merge
Lab: Containerise this service using the repo's Dockerfile as a template. Add one CI step of your own (for example: fail the build if a secret-looking string is committed).
Run: python 05_serving_and_config.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Engineer · Demo 5 — Serving: a config-driven prediction API with health, secrets hygiene and CI checks")
import os, re, warnings; warnings.filterwarnings("ignore"); from fastapi import FastAPI; from fastapi.testclient import TestClient; from pydantic import BaseModel, Field
os.environ.setdefault("MODEL_VERSION", "churn-lr:1.0"); os.environ.setdefault("THRESHOLD", "0.5"); X, y, names = ml.make_churn(); model = ml.LogReg(epochs=120).fit(X, y)
class Customer(BaseModel):
    tenure_months: float = Field(ge=0, le=600); monthly_bill: float = Field(ge=0, le=5000); support_tickets: int = Field(ge=0); late_payments: int = Field(ge=0); uses_app: int = Field(ge=0, le=1); contract_annual: int = Field(ge=0, le=1)
svc = FastAPI()
@svc.get("/health")
def health(): return {"ok": True, "model": os.environ["MODEL_VERSION"]}
@svc.post("/predict")
def predict(c: Customer):
    p = model.proba([[c.tenure_months, c.monthly_bill, c.support_tickets, c.late_payments, c.uses_app, c.contract_annual]])[0]; return {"churn_probability": round(p, 3), "flag": p >= float(os.environ["THRESHOLD"]), "model": os.environ["MODEL_VERSION"]}
t = TestClient(svc); print("GET /health  →", t.get("/health").json()); good = dict(tenure_months=3, monthly_bill=95, support_tickets=4, late_payments=2, uses_app=0, contract_annual=0)
print("POST /predict (risky customer) →", t.post("/predict", json=good).json()); r = t.post("/predict", json={**good, "monthly_bill": -5}); print(f"POST /predict (bill = -5)       → HTTP {r.status_code}: {r.json()['detail'][0]['msg']}")
os.environ["THRESHOLD"] = "0.8"; print("Same request after THRESHOLD=0.8 in config (no redeploy of code) →", t.post("/predict", json=good).json()["flag"])
hr(); SRC = 'API_KEY = "sk-live-9f8a7b6c5d4e3f2a1b0c"\npassword = os.getenv("DB_PASSWORD")\n'; leaks = re.findall(r"(?i)(api[_-]?key|secret|password)\s*=\s*[\"'][^\"']{8,}[\"']", SRC); print(f"Secrets scan on a sample file: {len(leaks)} hard-coded secret(s) found → build FAILS. Secrets live in the environment, never in git.")
print("\nCI gate for every merge:  lint · unit tests · schema tests · secrets scan · docker build · /health smoke test · image tagged with git SHA")
say("Behaviour that changes often belongs in config. Secrets belong in the environment. Neither belongs in the code.")
