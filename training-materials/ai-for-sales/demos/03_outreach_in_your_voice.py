"""AI for Sales · Demo 3 — Outreach in your voice: three variants, checked (12 min) · Module 3
Shows: three outreach variants built from voice sample + trigger + one ask, each checked against the voice guide and for unsupported claims
Lab: Paste three of your own best emails as the exemplar, write your banned-phrase list, and test a draft. What did it catch?
Run: python 03_outreach_in_your_voice.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Sales · Demo 3 — Outreach in your voice: three variants, checked")
GUIDE = {"banned": ["I hope this email finds you well", "synergy", "circle back", "revolutionary", "just checking in"], "max_sentence_words": 20, "must_have_cta": True, "exemplar": "Saw you opened three warehouses this quarter. We helped Kaveri cut mis-routes by 18% after a similar expansion. Worth a 20-minute call next week?"}
FACTS = {"case_kaveri": "Kaveri Pharma cut mis-routes by 18% in 2025", "sla": "99.2% on-time delivery in FY26"}
V = {"A — trigger-led": "Anita, congratulations on the three new warehouses. Kaveri cut mis-routes by 18% after a similar expansion. Can I show you how in 20 minutes next week? Reply with a time that suits.",
     "B — generic": "I hope this email finds you well! We are the leading, revolutionary logistics partner with guaranteed 100% on-time delivery and amazing synergy! Just checking in to circle back on our offering which I believe would be a truly excellent fit for your esteemed organisation across all of its many divisions.",
     "C — proof-led": "Anita, we run 99.2% on-time delivery. New warehouses usually mean new exceptions. Book a 20-minute review of your first month's data?"}
for n, d in V.items():
    v = text.voice_check(d, GUIDE); cl = text.check_claims(d, FACTS); print(f"\n{n}\n  {d}\n  voice: {'PASS' if v['pass'] else 'FAIL — ' + '; '.join(v['issues'])}  (similarity to your exemplar {v['similarity_to_exemplar']})")
    [print(f"  claim: {c['status']:<22} {c['claim'][:70]}") for c in cl]
say("Voice sample, one trigger, one ask. And every number in the email must be one you could defend on the call.")
