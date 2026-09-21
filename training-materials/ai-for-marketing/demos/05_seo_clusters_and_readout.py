"""AI for Marketing · Demo 5 — SEO clusters and an analytics read-out you can verify (12 min) · Module 5
Shows: search terms clustered into content briefs, and an analytics read-out where every statement is recomputed from the table
Lab: Export 30 of your real search queries and last month's channel table. Let AI write the read-out, then verify each sentence against the numbers.
Run: python 05_seo_clusters_and_readout.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Marketing · Demo 5 — SEO clusters and an analytics read-out you can verify")
KW = ["ai address verification", "address verification api india", "reduce misrouted parcels", "misrouted parcel cost", "cold chain logistics software", "cold chain compliance india", "logistics cost per order", "how to calculate logistics cost per order", "parcel misroute reasons"]
for head, kws in text.cluster_keywords(KW).items(): print(f"  BRIEF: {head:<12} ← {', '.join(kws)}")
hr(); DATA = [("Organic search", 4200, 126), ("LinkedIn", 1800, 27), ("Email", 950, 57), ("Paid search", 2600, 39)]; table(["Channel", "Visits", "Leads", "Conversion"], [[c, v, l, f"{l / v:.1%}"] for c, v, l in DATA])
CLAIMS = [("Email converts best", max(DATA, key=lambda d: d[2] / d[1])[0] == "Email"), ("Organic brings the most leads", max(DATA, key=lambda d: d[2])[0] == "Organic search"), ("LinkedIn converts better than paid search", DATA[1][2] / DATA[1][1] > DATA[3][2] / DATA[3][1]), ("Paid search drives half of all leads", DATA[3][2] / sum(d[2] for d in DATA) >= 0.5)]
print("\nAI read-out, verified line by line:"); [print(f"  [{'TRUE ' if ok else 'FALSE'}] {c}") for c, ok in CLAIMS]
say("AI is a fast analyst and a confident one. Recompute every sentence you plan to repeat to your boss.")
