"""AI for All · Demo 1 — the confident wrong answer, then the same question with the right page (5 min).
Run: python demos/01_confident_wrong.py"""
import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "agentic-ai-workshop" / "demos"))
from common import *
banner("AI for All · Demo 1 — closed book vs open book")
q = "How many days of annual leave do employees at Acme Logistics get, and can they carry days over?"
print(f"Q: {q}\n\nCLOSED BOOK (no documents):")
print("   " + ((llm.complete(f"Answer in two sentences: {q}", max_tokens=100) or "").strip() if LIVE else "'Acme Logistics employees receive 15 days of annual leave and may carry over up to 10 days.'  ← fluent, confident, invented"))
print("\nOPEN BOOK (the policy page is on the desk):")
docs = load_docs(); chunks = [c for d in docs for c in chunk_by_heading(d)]; top = [c for _, c in bm25(q, chunks)[:2]]
print("   " + answer(q, top)[0])
print("\nSay it: 'It wasn't lying. It had nothing to go on. Give it the page.'")
