"""Agentic AI Engineer · Demo 6 — Multi-agent and computer use: supervisor/worker fan-out — and when not to (25 min) · Module 6
Shows: a supervisor that fans a research task out to three workers in parallel, merges with conflict detection, and the token bill compared with a single agent
Lab: For your capstone: justify in three sentences why you need more than one agent. If you cannot, build one agent with better tools.
Run: python 06_supervisor_workers.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Agentic AI Engineer · Demo 6 — Multi-agent and computer use: supervisor/worker fan-out — and when not to")
SOURCES = {"pricing": "Vendor A: INR 360/user/year. Vendor B: INR 410/user/year, 10% off above 500 users.", "security": "Vendor A: ISO 27001, India region. Vendor B: SOC 2, no India region until 2027.", "references": "Vendor A: 2 logistics references. Vendor B: 5 references, none in logistics. Vendor A price is INR 300/user/year."}
def worker(topic):
    txt = SOURCES[topic]; import re; facts = {("A" if "Vendor A" in s else "B", topic): s.strip() for s in re.split(r"(?<=\.)\s+", txt) if s.startswith("Vendor")}; return facts, cost(1800, 250)
print("SUPERVISOR plan: split by topic → 3 workers in parallel → merge → check conflicts → one answer\n"); merged = {}; spend = cost(1200, 300)
for t in SOURCES:
    f, c_ = worker(t); spend += c_; print(f"  worker[{t}] → {len(f)} finding(s), ${c_:.4f}"); merged.update({(k[0], t): v for k, v in f.items()}); extra = [s for s in SOURCES[t].split(". ") if "price is" in s]
    if extra: merged[("A", "pricing-2")] = extra[0]
import re; prices = {k: re.search(r"INR (\d+)", v).group(1) for k, v in merged.items() if "pricing" in k[1] and k[0] == "A"}; conflict = len(set(prices.values())) > 1
print(f"\n  MERGE: {len(merged)} findings · conflict check: {'CONFLICT — Vendor A price reported as INR ' + ' and INR '.join(sorted(set(prices.values()))) + ' → ask a human / re-verify, do NOT average' if conflict else 'none'}")
single = cost(1200 + 3 * 1800 + 1500, 600); print(f"\n  Cost: supervisor + 3 workers ${spend + cost(2500, 400):.4f} vs one agent doing it serially ${single:.4f} → multi-agent is {(spend + cost(2500, 400)) / single:.1f}× the tokens, but ~3× faster wall-clock.")
print("\nUse multi-agent when: the work is truly parallel · contexts would not fit one window · different permissions per worker.\nDo NOT when: steps depend on each other · one agent with better tools would do · you cannot evaluate a single agent yet.")
print("Computer-use agents: slowest and most fragile interface — use only when there is no API; sandbox them; never give them a logged-in finance session.")
say("Multi-agent systems multiply tokens, latency and failure modes. Earn them with a single agent that already works.")
