#!/usr/bin/env python3
"""Provisioning worker: runs queued tenant environments and the nightly expiry, in a loop. Runs as the `worker` container in production;
`python scripts/provision_worker.py --once` for cron or by hand. Idempotent: a job that already ran does nothing."""
import sys, time, datetime as dt, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from app.core import db; from app.services.platform import engine
db.init(); once = "--once" in sys.argv; last_nightly = None
while True:
    for r in engine.run_jobs(): print(f"[{dt.datetime.now():%H:%M:%S}] {r['job_id']} {r['tenant_id']} {r['status']}" + (f" — {r['error']}" if r.get("error") else ""), flush=True)
    if last_nightly != dt.date.today():
        for line in engine.expire_due(): print("nightly:", line, flush=True)
        last_nightly = dt.date.today()
    if once: break
    time.sleep(30)
