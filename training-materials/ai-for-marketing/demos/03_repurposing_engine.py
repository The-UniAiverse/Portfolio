"""AI for Marketing · Demo 3 — One piece → six assets, numbers intact (12 min) · Module 3
Shows: a long article repurposed into six formats with per-format limits, then a consistency check that every number survived unchanged
Lab: Take one real long-form piece. Produce the six assets, then run the consistency check by eye: did any number, name or claim drift?
Run: python 03_repurposing_engine.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Marketing · Demo 3 — One piece → six assets, numbers intact")
import re; art = data_path(__file__, "article.md").read_text(); title = art.splitlines()[0].lstrip("# ")
out = text.repurpose(art, title)
if "live" in out: print(out["live"])
else:
    for k, v in out.items(): print(f"\n[{k}]  " + (f"({len(v)} chars)" if isinstance(v, str) else f"({len(v)} items)")); print("  " + (v if isinstance(v, str) else "\n  ".join(v)))
hr(); src = set(re.findall(r"\d[\d,]*%?", art)); flat = " ".join(v if isinstance(v, str) else " ".join(v) for v in out.values()); used = set(re.findall(r"\d[\d,]*%?", flat))
print(f"Numbers in source: {sorted(src)}\nNumbers in assets: {sorted(used)}\nInvented numbers : {sorted(used - src) or 'none'}")
LIMITS = {"tweet": 240, "linkedin": 400, "email_body": 520}; [print(f"  {k:<11} {len(out[k]):>3}/{v} chars {'ok' if len(out[k]) <= v else 'OVER'}") for k, v in LIMITS.items() if k in out and isinstance(out[k], str)]
say("Six assets, one source of truth. If a number changes between the article and the tweet, you have a fact-checking problem, not a content engine.")
