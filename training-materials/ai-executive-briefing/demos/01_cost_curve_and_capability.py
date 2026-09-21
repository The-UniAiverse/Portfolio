"""AI Executive & Board Briefing · Demo 1 — What changed: the cost curve, in your numbers (8 min) · Module 1
Shows: what one million customer questions cost across three model classes and three designs — the number that reshapes a business case
Lab: Before the session the facilitator replaces VOLUME with the client's own annual contact volume.
Run: python 01_cost_curve_and_capability.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Executive & Board Briefing · Demo 1 — What changed: the cost curve, in your numbers")
VOLUME = arg("--volume", 1_000_000, int); designs = [("Simple answer", 1400, 200), ("Grounded on your documents", 5100, 400), ("Agent, six steps", 42000, 4000)]
table(["Design \\ model class", "cheap", "mid", "flagship"], [[n] + [money(cost(i, o, t) * VOLUME) for t in ("cheap", "mid", "flagship")] for n, i, o in designs])
lo, hi = cost(1400, 200, "cheap") * VOLUME, cost(42000, 4000, "flagship") * VOLUME; print(f"\n  Same {VOLUME:,} questions: {money(lo)} to {money(hi)} — a {hi / lo:,.0f}× spread decided by design choices, not by the vendor.")
print(f"  Human handling at $2.50 a contact: {money(2.5 * VOLUME)}.  Rates are placeholders in labkit RATES — verify quarterly before quoting.")
say("The board question is no longer 'can AI do this'. It is 'which design, at what unit cost, with what control'.")
