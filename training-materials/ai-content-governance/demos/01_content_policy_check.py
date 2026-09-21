"""AI Content Governance & Brand Safety · Demo 1 — Rules for generated content: a policy you can run (15 min) · Module 1
Shows: a content policy as data applied to five assets: disclosure, provenance record, IP/licence and regulated claims — with the rule that failed
Lab: Draft your own POLICY in ten lines. Test it on five recent assets. Which rule produced the most failures — and is the rule wrong, or the practice?
Run: python 01_content_policy_check.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Content Governance & Brand Safety · Demo 1 — Rules for generated content: a policy you can run")
POLICY = {"disclose_if": ["synthetic_person", "ai_voice", "fully_ai_text_customer_facing"], "provenance_required": True, "licence_required_for": ["stock", "third_party"], "regulated_words": ["cure", "guaranteed returns", "risk-free"]}
A = [dict(name="Blog: address quality", kind="text", ai="assisted", provenance="prompt+sources logged", words=""), dict(name="Ad: smiling 'customer' photo", kind="image", ai="synthetic_person", provenance="", disclosure=False, words=""),
     dict(name="Explainer video voice-over", kind="audio", ai="ai_voice", provenance="tool+script logged", disclosure=True, words=""), dict(name="Investor one-pager", kind="text", ai="fully_ai_text_customer_facing", provenance="logged", disclosure=True, words="guaranteed returns"),
     dict(name="Social image from stock site", kind="image", ai="none", source="stock", licence="", provenance="n/a", words="")]
rows = []
for a in A:
    f = []
    if a["ai"] in POLICY["disclose_if"] and not a.get("disclosure"): f.append("disclosure missing")
    if POLICY["provenance_required"] and a["ai"] != "none" and not a.get("provenance"): f.append("no provenance record")
    if a.get("source") in POLICY["licence_required_for"] and not a.get("licence"): f.append("no licence on file")
    f += [f"regulated claim: '{w}'" for w in POLICY["regulated_words"] if w in a["words"]]; rows.append([a["name"], a["ai"], "PASS" if not f else "FAIL", "; ".join(f) or "—"])
table(["Asset", "AI involvement", "Result", "Rule that failed"], rows)
print("\n  Provenance record = who, which tool, which prompt, which sources, who approved. It is the only thing that lets you answer 'where did this come from?' six months later.")
say("A content policy nobody can test is a poster. Write it as rules you can run against an asset.")
