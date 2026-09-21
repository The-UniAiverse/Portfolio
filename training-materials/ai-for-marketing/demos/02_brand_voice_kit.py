"""AI for Marketing · Demo 2 — Brand voice kit: test drafts against your voice (12 min) · Module 2
Shows: a voice guide as data (banned phrases, sentence length, exemplar) used to score three drafts, with the specific fixes
Lab: Build your kit: three exemplars, ten banned phrases, one sentence-length rule. Test a draft from last month. Would you have published it?
Run: python 02_brand_voice_kit.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Marketing · Demo 2 — Brand voice kit: test drafts against your voice")
GUIDE = {"banned": ["game-changing", "leverage", "in today's fast-paced world", "unlock", "seamless", "cutting-edge"], "max_sentence_words": 22, "must_have_cta": True, "exemplar": open(data_path(__file__, "article.md")).read()}
DRAFTS = {"Human, on-voice": "Kaveri ships medicines to 2,300 pharmacies. Mis-routes cost them INR 9 lakh a month. An address check at label printing cut that by 18% in 90 days. See how the morning exception report works.",
          "AI, no guidance": "In today's fast-paced world, leverage our game-changing, cutting-edge AI to unlock seamless logistics excellence across your entire end-to-end supply chain ecosystem and transform the way that you and all of your stakeholders think about delivery!!",
          "AI, with the kit": "Mis-routed parcels are expensive. Kaveri cut theirs by 18% in 90 days with one change at label printing. Download the two-page case study."}
for n, d in DRAFTS.items():
    v = text.voice_check(d, GUIDE); print(f"\n{n}  —  {'PASS' if v['pass'] else 'FAIL'}  (overlap with exemplar {v['similarity_to_exemplar']})\n  {d}"); [print(f"    ✗ {i}") for i in v["issues"]]
say("The model has no voice. It borrows the one you give it — so give it three good examples and a list of words you never use.")
