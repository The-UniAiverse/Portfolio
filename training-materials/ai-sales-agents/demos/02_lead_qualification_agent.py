"""AI Agents for Sales Operations · Demo 2 — A lead-qualification agent with tools, scopes and an approval gate (20 min) · Module 2
Shows: an agent that enriches, scores and routes a lead using three read tools and one write tool gated by human approval — plus what happens when it tries something out of scope
Lab: Rebuild this flow in your CRM's AI / automation platform. List every tool you gave it and mark each read or write. Which writes need approval?
Run: python 02_lead_qualification_agent.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Agents for Sales Operations · Demo 2 — A lead-qualification agent with tools, scopes and an approval gate")
FIRMO = {"zenithfoods.in": {"employees": 1200, "industry": "FMCG", "warehouses": 9}, "tinybakery.in": {"employees": 8, "industry": "Food", "warehouses": 0}}
LOG = []
tools = [agent.Tool("lookup_company", "Firmographic data for a domain", {"domain": {"type": "string"}}, lambda domain: FIRMO.get(domain, "no data")),
         agent.Tool("score_lead", "Score 0-100 from employees and warehouses", {"employees": {"type": "number"}, "warehouses": {"type": "number"}}, lambda employees, warehouses: min(100, employees // 20 + warehouses * 6)),
         agent.Tool("check_crm_duplicate", "Is this domain already an account?", {"domain": {"type": "string"}}, lambda domain: "existing account: Zenith Foods (owner: Priya)" if "zenith" in domain else "no match"),
         agent.Tool("assign_owner", "WRITE: assign the lead to a rep in the CRM", {"domain": {"type": "string"}, "owner": {"type": "string"}}, lambda domain, owner: LOG.append((domain, owner)) or f"assigned {domain} → {owner}", destructive=True, scope="write")]
def plan_for(domain):
    return agent.scripted([{"think": "Who is this company?", "tool": "lookup_company", "args": {"domain": domain}},
        lambda h: {"think": "Score it from the facts I just read.", "tool": "score_lead", "args": {"employees": eval(h[0]["obs"])["employees"], "warehouses": eval(h[0]["obs"])["warehouses"]}},
        {"think": "Never create a duplicate — check the CRM.", "tool": "check_crm_duplicate", "args": {"domain": domain}},
        lambda h: ({"think": "Existing account: route to its owner.", "tool": "assign_owner", "args": {"domain": domain, "owner": "Priya"}} if "existing" in h[2]["obs"] else
                   {"think": "Small and new: route to the SMB queue.", "tool": "assign_owner", "args": {"domain": domain, "owner": "SMB queue"}} if int(h[1]["obs"]) < 40 else {"think": "Enterprise, new.", "tool": "assign_owner", "args": {"domain": domain, "owner": "Enterprise desk"}}),
        lambda h: {"think": "Done.", "answer": f"score {h[1]['obs']} · {h[3]['obs']}"}])
for dom in ("zenithfoods.in", "tinybakery.in"):
    print(f"\nLEAD: {dom}"); r = agent.run_agent(f"qualify {dom}", tools, plan_for(dom)); print(f"  RESULT {r.answer}")
hr(); print("Same agent, write scope removed (pilot week 1 — read-only):"); r = agent.run_agent("qualify zenithfoods.in", tools, plan_for("zenithfoods.in"), caps=agent.Caps(allowed_scopes=("read",)), verbose=False)
print(f"  write attempts blocked: {sum(1 for s in r.steps if s.get('blocked'))} · CRM changes made: {len(LOG) - 2}")
say("Start read-only. Earn write access one tool at a time, with a person on the gate.")
