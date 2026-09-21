"""MLOps & LLMOps · Demo 2 — LLMOps: version the whole RAG stack — prompt, embeddings, index, model (25 min) · Module 2
Shows: a stack manifest that pins and hashes everything that changes an answer, a diff between two releases, the eval gate it triggers, and a provider model update handled as a change
Lab: Write the manifest for your own LLM app. Change one thing (the prompt). Which evals must re-run before it ships? Who approves?
Run: python 02_version_a_rag_stack.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("MLOps & LLMOps · Demo 2 — LLMOps: version the whole RAG stack — prompt, embeddings, index, model")
docs = [d for d in load_docs() if "draft" not in d["id"].lower()]; P1 = GROUNDING; P2 = GROUNDING + " Answer in at most three sentences."
A = ops.stack_manifest(P1, "embed-small-v3@2026-02", {"strategy": "heading", "prefix": True}, [d["text"] for d in docs], "mid-model-2026-05"); B = ops.stack_manifest(P2, "embed-small-v3@2026-02", {"strategy": "heading", "prefix": True}, [d["text"] for d in docs], "mid-model-2026-08")
print("Release 14 manifest:"); [print(f"  {k:<16}{v}") for k, v in A.items()]; print(f"\nRelease 15 changes vs 14  (stack {A['stack_version']} → {B['stack_version']}):"); [print(f"  • {x}") for x in ops.diff_manifest(A, B)]
RULES = {"prompt": "answer evals (correctness, faithfulness, refusal)", "llm_model": "FULL eval suite + cost/latency check + red-team probe", "embedding_model": "RE-EMBED the whole index + retrieval evals — old and new vectors cannot be mixed", "chunking": "re-index + retrieval evals", "index": "retrieval evals on changed documents"}
print("\nRequired before release:"); [print(f"  {x.split(':')[0]:<16}→ {RULES[x.split(':')[0]]}") for x in ops.diff_manifest(A, B)]
hr(); print("Provider notice: 'mid-model-2026-05 will be retired on 2026-12-01; the alias now points to 2026-08.'\n  If you called the ALIAS, your system changed last night and nobody re-ran the evals.\n  If you PINNED the dated version, nothing changed — and you have until 1 Dec to test the new one on your golden set.")
say("In LLM systems the model is the smallest part of the version. Pin everything that can change an answer.")
