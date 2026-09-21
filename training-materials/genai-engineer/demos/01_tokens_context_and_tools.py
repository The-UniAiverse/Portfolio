"""GenAI Engineer · Demo 1 — LLM fundamentals for builders: context budget and tool-schema cost (20 min) · Module 1
Shows: a request's context budget broken down line by line, what 5 vs 25 tool schemas cost on every call, and prompt patterns tested instead of believed
Lab: Measure your own system prompt and tool list. What share of every request is overhead before the user has typed a word?
Run: python 01_tokens_context_and_tools.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("GenAI Engineer · Demo 1 — LLM fundamentals for builders: context budget and tool-schema cost")
SYS = "You are the Acme support assistant. " * 40; tools = [agent.Tool(f"tool_{i}", "Look up a record in system %d and return its status, owner, dates and notes" % i, {"id": {"type": "string"}, "fields": {"type": "string"}}, lambda **k: "") for i in range(25)]
hist = "user: where is my parcel? assistant: It left Pune at 09:40. " * 12; ctx = " ".join(c["text"] for d in load_docs()[:2] for c in chunk_by_heading(d))[:6000]; q = "Can I claim for a parcel that arrived broken yesterday?"
for n_tools in (5, 25):
    parts = [("system prompt", tokens(SYS)), (f"{n_tools} tool schemas", sum(t.schema_tokens() for t in tools[:n_tools])), ("retrieved context", tokens(ctx)), ("chat history", tokens(hist)), ("the actual question", tokens(q))]; tot = sum(v for _, v in parts)
    print(f"\nWith {n_tools} tools — {tot:,} input tokens per call (${cost(tot, 300):.4f}):"); [print(f"  {k:<22}{bar(v, tot, 30)} {v:>5} ({v / tot:.0%})") for k, v in parts]
hr(); print("Prompt patterns — tested on the 14-question sheet, not believed:")
import csv, pathlib; tests = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parents[2] / "agentic-ai-workshop/demos/test_sheet.csv"))); ch = [c for d in load_docs() if "draft" not in d["id"].lower() for c in chunk_by_heading(d)]
def run(k): return sum(evals.correctness(grounded(t["question"], rerank(t["question"], [c for _, c in rrf(bm25(t["question"], ch), semantic(t["question"], ch))[:8]], k))[0], t["expected"]) >= 0.6 or (t["type"] == "out_of_scope") for t in tests)
for label, k in (("top-1 context", 1), ("top-3 context", 3), ("top-6 context (more is better?)", 6)): print(f"  {run(k):>2}/{len(tests)}  {label}")
say("The question is 1% of the request. Everything else is a design decision you are paying for on every call.")
