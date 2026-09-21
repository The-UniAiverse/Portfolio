"""AI for All · Demo 3 — Which tasks suit AI? Sort 20 (10 min) · Module 3
Shows: a transparent rule set that sorts everyday tasks into AI-suitable / AI-with-checking / not-for-AI, with the reason
Lab: Each table adds five of its own tasks to TASKS and re-runs. Argue with two verdicts and change the rule, not the verdict.
Run: python 03_task_sorter.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for All · Demo 3 — Which tasks suit AI? Sort 20")
TASKS = [("Draft a polite reply to a late supplier", "draft"), ("Summarise a 12-page policy for the team", "summarise"), ("Translate a notice into Hindi and Marathi", "translate"),
         ("Brainstorm 20 names for the offsite", "brainstorm"), ("Count how many invoices are overdue in a spreadsheet", "count"), ("Tell me today's USD-INR rate", "live_fact"),
         ("Decide whether to approve Ramesh's loan", "decide_person"), ("Rewrite my CV bullet points", "draft"), ("What is our notice period? (no document given)", "company_fact"),
         ("Explain a contract clause in plain words", "explain"), ("Add up a column of 400 expense lines", "count"), ("Write the first draft of a project update", "draft"),
         ("Diagnose my chest pain", "decide_person"), ("Turn meeting notes into action items", "extract"), ("Predict next month's exact sales figure", "predict"),
         ("Check a paragraph for tone before sending", "review"), ("Find the clause about termination in this PDF (attached)", "extract"), ("Who won yesterday's match?", "live_fact"),
         ("Create a quiz from this training manual (attached)", "extract"), ("Sign off the safety inspection", "decide_person")]
RULES = {"draft": ("AI-suitable", "language work; you edit the result"), "summarise": ("AI-suitable", "give it the document; spot-check numbers"), "translate": ("AI + checking", "good first pass; a speaker checks names and legal terms"),
         "brainstorm": ("AI-suitable", "quantity is the point; you choose"), "explain": ("AI + checking", "useful, but confirm anything you will act on"), "extract": ("AI-suitable", "the answer is in the text you supply"),
         "review": ("AI-suitable", "a second pair of eyes"), "count": ("Not for AI alone", "it predicts text, it does not calculate — use a spreadsheet or a tool-using assistant"),
         "live_fact": ("Not for AI alone", "no live data inside the model — needs search or a system"), "company_fact": ("Not for AI alone", "it has never seen your documents — it will guess confidently"),
         "predict": ("Not for AI alone", "a forecast needs your data and a model built for it"), "decide_person": ("Human decides", "affects a person's rights, money or health — AI may assist, never decide")}
order = ["AI-suitable", "AI + checking", "Not for AI alone", "Human decides"]
for verdict in order:
    rows = [(t, RULES[k][1]) for t, k in TASKS if RULES[k][0] == verdict]; print(f"\n{verdict.upper()}  ({len(rows)})"); table(["Task", "Why"], [list(r) for r in rows])
hr(); print("The pattern: AI is strong where the ANSWER IS LANGUAGE and you can check it; weak where the answer is a FACT it was never given or a NUMBER it must compute.")
say("Ask two questions: is the answer in what I gave it, and can I check it in a minute?")
