"""Advanced, Hybrid & Agentic RAG · Demo 2 — GraphRAG: multi-hop questions a vector search cannot answer (25 min) · Module 3
Shows: a small knowledge graph built from policy facts, used to answer multi-hop and 'who is affected' questions that flat retrieval misses — plus table-aware chunking
Lab: Write five multi-hop questions about your own organisation (who approves X for people in Y?). Try them on plain RAG first. Which entities and relations would your graph need?
Run: python 02_graph_multihop.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Advanced, Hybrid & Agentic RAG · Demo 2 — GraphRAG: multi-hop questions a vector search cannot answer")
T = [("Claims Committee", "reviews", "claims above INR 10,000"), ("Claims Committee", "meets", "weekly"), ("Claims Committee", "chaired_by", "Head of Claims"), ("Head of Claims", "reports_to", "COO"), ("damage claim", "requires", "photographs + packing slip"), ("damage claim", "deadline", "48 hours"),
     ("damage claim", "is_a", "claim"), ("lost shipment", "is_a", "claim"), ("lost shipment", "refund", "full declared value"), ("Pune hub", "handles", "SH-1042"), ("SH-1042", "has_claim", "damage claim"), ("SH-1042", "claim_value", "INR 14,000")]
G = {}
for s, r, o in T: G.setdefault(s, []).append((r, o))
def hop(start, *rels):
    node = start; path = [start]
    for r in rels:
        nxt = next((o for rel, o in G.get(node, []) if rel == r), None)
        if nxt is None: return path, None
        node = nxt; path.append(f"—{r}→ {nxt}")
    return path, node
print("Q: Who is ultimately accountable for the decision on the claim for SH-1042, and when will it be looked at?\n")
ch = [c for d in load_docs() if "draft" not in d["id"].lower() for c in chunk_by_heading(d)]; a = grounded("Who is accountable for the claim decision on SH-1042 and when?", [c for _, c in rrf(bm25("claim SH-1042 accountable", ch), semantic("claim decision", ch))[:3]])[0]
print(f"  Plain RAG   : {a[:140]}\n                (it has never seen SH-1042 next to the committee — the link lives in two systems)\n")
p1, val = hop("SH-1042", "claim_value"); big = int(val.replace("INR ", "").replace(",", "")) > 10000; p2, who = hop("Claims Committee", "chaired_by", "reports_to"); _, when = hop("Claims Committee", "meets")
print(f"  GraphRAG    : {' '.join(p1)}  → {'above' if big else 'below'} INR 10,000 → goes to the Claims Committee\n                {' '.join(p2)}\n  ANSWER      : The Claims Committee ({when}); chaired by the Head of Claims, accountable to the {who}.")
hr(); TABLE = "| Region | SLA hours | Refund % |\n|---|---|---|\n| Metro | 24 | 100 |\n| Tier-2 | 48 | 100 |\n| Remote | 96 | 50 |"; print("Tables: naive chunking cuts rows from their header.\n"); rows = [r.strip("| ").split(" | ") for r in TABLE.splitlines() if not r.startswith("|---")]; hdr = rows[0]
[print("  chunk: " + "; ".join(f"{h} = {v}" for h, v in zip(hdr, r))) for r in rows[1:]]; print("\n  Each row becomes a self-describing sentence — now 'what is the SLA for remote areas?' retrieves '96'.")
say("Vector search finds passages that look like the question. A graph finds answers that need two facts from two places.")
