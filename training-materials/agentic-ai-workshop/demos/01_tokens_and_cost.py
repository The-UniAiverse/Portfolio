"""DEMO 1 — Tokens and the cost of one question (Module 2-3, ~10 min on screen).
Run: python 01_tokens_and_cost.py [--daily 300]"""
import sys; from common import *

banner("Demo 1 · Tokens & the cost of one question")
daily = int(sys.argv[sys.argv.index("--daily") + 1]) if "--daily" in sys.argv else 300
samples = ["The contract was terminated.", "The contract was NOT terminated.", "ERR_SVC_4471", "Refund policy for damaged goods, section 3, effective January 2026."]
print("A token is ~¾ of a word. Watch how the count grows:\n")
for s in samples: print(f"  {tokens(s):>3} tokens  ←  {s!r}")
hr()
print("One RAG question, per request:")
parts = {"System / instructions": 1000, "5 retrieved chunks": 2500, "Conversation so far": 1500, "The question": 100}
inp = sum(parts.values()); out = 400
for k, v in parts.items(): print(f"  {k:<24}{v:>7,} tokens")
print(f"  {'Sent in':<24}{inp:>7,}\n  {'Answer written back':<24}{out:>7,}")
hr()
for tier in RATES:
    c = cost(inp, out, tier); print(f"  {tier:<9} ${c:.4f} / question   → {daily}/day ≈ ${c * daily * 30:,.0f} / month")
hr()
print("The two explosions:")
c_hist = cost(inp - 1500 + 30000, out); c_flag = cost(inp, out, "flagship")
print(f"  Untrimmed history (30k tokens):  ${c_hist:.4f} / question  ({c_hist / cost(inp, out):.0f}×)")
print(f"  Flagship model for everything:   ${c_flag:.4f} / question  ({c_flag / cost(inp, out):.0f}×)")
print("\nSay it: 'You don't pay per question. You pay per token. Design the prompt like you'd design a bill.'")
