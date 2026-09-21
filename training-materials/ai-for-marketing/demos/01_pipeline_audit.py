"""AI for Marketing · Demo 1 — Content pipeline audit: where the days go (8 min) · Module 1
Shows: a content pipeline mapped stage by stage with elapsed days vs working hours, showing where AI helps and where the queue is the real problem
Lab: Map your own last three pieces of content. Where did each wait longest? Is that a writing problem or an approval problem?
Run: python 01_pipeline_audit.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Marketing · Demo 1 — Content pipeline audit: where the days go")
P = [("Brief", 1.5, 3, 0.5), ("First draft", 6, 4, 0.7), ("Review & legal", 1, 9, 0.1), ("Design", 3, 4, 0.3), ("Publish & distribute", 1.5, 1, 0.5), ("Measure", 1, 7, 0.6)]
table(["Stage", "Work hours", "Elapsed days", "AI can take", "Hours after AI"], [[n, h, d, f"{a:.0%}", f"{h * (1 - a * .75):.1f}"] for n, h, d, a in P])
th, td = sum(p[1] for p in P), sum(p[2] for p in P); ah = sum(h * (1 - a * .75) for _, h, _, a in P); print(f"\n  Work: {th} h → {ah:.1f} h with AI ({1 - ah / th:.0%} less).  Elapsed: {td} days → about {td - 3} days.")
print("  AI halves the writing. It barely touches the 9 days in review. Fix the queue: a pre-publish checklist legal has already agreed (see Demo 6).")
say("If review takes nine days, a faster first draft gets you to the queue sooner. That is all.")
