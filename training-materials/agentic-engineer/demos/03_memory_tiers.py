"""Agentic AI Engineer · Demo 3 — Memory: short-term, working, long-term, episodic — and what each costs (20 min) · Module 3
Shows: a 12-turn conversation run with and without memory tiers: context tokens per turn, what is remembered, and recall of a fact stated ten turns earlier
Lab: Decide for your agent: what goes in working memory, what is written to long-term, and who can delete it. Test recall of a preference after 20 turns.
Run: python 03_memory_tiers.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Agentic AI Engineer · Demo 3 — Memory: short-term, working, long-term, episodic — and what each costs")
TURNS = ["I'm Anita from Zenith Foods.", "We prefer deliveries before 10 am.", "Our account manager is Priya.", "Can you check SH-1042?", "And SH-2210?", "What about last week's claim?", "Please note our Pune dock is closed on Sundays.", "Any delays today?",
         "Send me the August summary.", "Who handles claims above 10,000?", "Thanks.", "Book tomorrow's pickup — what time suits us best?"]
full = []; mem = agent.Memory(window=4); rows = []
for i, t in enumerate(TURNS, 1):
    full.append(t); mem.add_turn("user", t)
    if any(w in t.lower() for w in ("prefer", "closed on", "account manager", "i'm ")): mem.remember(t, tags=[w for w in ("delivery", "time", "pickup", "dock", "sunday", "manager") if w in t.lower() or (w in ("delivery", "time", "pickup") and "deliver" in t.lower())])
    rows.append([i, sum(tokens(x) for x in full) + 40 * i, mem.context_tokens() + sum(tokens(f) for f in mem.recall(t)) + 40 * min(i, 4)])
table(["Turn", "Tokens: send whole history", "Tokens: window + recalled facts"], rows[::2] + [rows[-1]])
q = TURNS[-1]; print(f"\nTurn 12: '{q}'\n  window-only agent sees: {[t for _, t in mem.short]}\n  → it has forgotten the 10 am preference (turn 2).\n  long-term recall → {mem.recall('delivery pickup time')}")
print(f"  episodic summary of dropped turns: {mem.episodes[:3]} …\n\n  Governance: long-term memory is personal data. It needs an owner, a retention period, and a 'forget me' path.")
say("Context is rent; memory is a filing cabinet. Pay rent only for what this turn needs, and file the rest where you can find it.")
