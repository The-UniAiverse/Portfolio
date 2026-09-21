"""Agentic AI Engineer · Demo 2 — Tools and MCP: schemas, token cost, scoping and vetting a server (25 min) · Module 2
Shows: tool schemas costed in tokens, argument validation rejecting bad calls, permission scopes, and a vetting checklist run against an MCP server manifest
Lab: Write the manifest for one internal MCP server you would like (three tools). Run the vetting checklist. Which tool would you refuse to expose in week one?
Run: python 02_tools_and_mcp_vetting.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Agentic AI Engineer · Demo 2 — Tools and MCP: schemas, token cost, scoping and vetting a server")
import json; M = json.loads(data_path(__file__, "mcp_manifest.json").read_text()); tools = [agent.Tool(t["name"], t["description"], t["params"], lambda **k: "ok", destructive=t.get("destructive", False), scope=t.get("scope", "read")) for t in M["tools"]]
table(["Tool", "Scope", "Destructive", "Schema tokens"], [[t.name, t.scope, t.destructive, t.schema_tokens()] for t in tools]); tot = sum(t.schema_tokens() for t in tools); print(f"\n  {tot} tokens of tool schemas on EVERY call → {money(cost(tot, 0) * 50000)} a month at 50,000 calls, before any work is done.")
hr(); print("Argument validation (the model will send wrong arguments; your runtime must not execute them):")
for name, args in [("crm_update_stage", {"deal_id": "D-19", "stage": "won"}), ("crm_update_stage", {"deal_id": "D-19", "stage": "definitely-won!!"}), ("crm_search", {"query": 42}), ("crm_delete_contact", {"id": "C-7", "force": True})]:
    t = next(x for x in tools if x.name == name); print(f"  {name}({args}) → {agent.validate_args(t, args) or 'valid'}")
hr(); V = [("Every tool has a description and typed params", all(t["description"] and t["params"] for t in M["tools"])), ("Write/delete tools are marked destructive", all(t.get("destructive") for t in M["tools"] if t.get("scope") in ("write", "delete"))), ("No tool takes free-form SQL / shell / URL", not any(p in ("sql", "command", "url") for t in M["tools"] for p in t["params"])),
     ("Server declares auth and per-user identity", M.get("auth") == "oauth-per-user"), ("Server is pinned to a version + publisher verified", bool(M.get("version")) and M.get("publisher_verified")), ("Tool descriptions contain no instructions to the model", not any(guard.injection_score(t["description"])[0] for t in M["tools"]))]
print("MCP server vetting:"); [print(f"  [{'x' if ok else ' '}] {n}") for n, ok in V]; bad = [t["name"] for t in M["tools"] if guard.injection_score(t["description"])[0]]; print(f"\n  → {'APPROVE' if all(ok for _, ok in V) else 'REJECT'}" + (f" — poisoned description in: {bad}" if bad else ""))
say("A tool description is a prompt written by someone else. Read it like one.")
