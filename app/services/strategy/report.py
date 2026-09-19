from __future__ import annotations
from pathlib import Path
from app.core.pdf import Doc

def to_markdown(r: dict) -> str:
    L = [f"# AI Strategy & Roadmap — {r['organisation']}", f"*{r['industry']} · {r['staff']} staff · uniAIverse*", "",
         f"**Ambition:** {r['ambition'] or '—'}", "", "## Executive summary", r["narrative"], "",
         "## Prioritised use-case backlog", "", "| # | Use case | Function | Pattern | V | F | R | Effort | Score | Quadrant | Horizon |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {b['rank']} | {b['name']} | {b['function']} | {b['pattern']} | {b['value']} | {b['feasibility']} | {b['risk']} | {b['effort']} | {b['score']} | {b['quadrant_title']} | {b['horizon']} |" for b in r["backlog"]]
    L += ["", "## Business cases", "", "| Use case | Build (USD) | Run / month | Weeks | Annual benefit | Year-1 net | Payback (months) | Basis |", "|---|---|---|---|---|---|---|---|"]
    for b in r["backlog"]:
        c = b["business_case"]
        L.append(f"| {b['name']} | {c['build_usd'][0]:,}–{c['build_usd'][1]:,} | {c['run_usd_month'][0]:,}–{c['run_usd_month'][1]:,} | {c['weeks'][0]}–{c['weeks'][1]} | {c['annual_benefit_usd']:,} | {c['year1_net_usd']:,} | {c['payback_months']} | {c['benefit_source']} |")
    if r["foundations"]:
        L += ["", "## Foundations required first"]
        for f in r["foundations"]: L += [f"### {f['title']} (readiness domain: {f['domain']})"] + [f"- {a}" for a in f["actions"]]
    L += ["", "## Roadmap"]
    for ph in r["phases"]: L += [f"### Phase {ph['id']} — {ph['title']} (months {ph['months']})", f"*{ph['goal']}*"] + [f"- {i}" for i in ph["items"]] + [""]
    om = r["operating_model"]
    L += ["## Operating model", f"**Recommended: {om['title']}** — fits {om['fits']}. Pros: {om['pros']}. Cons: {om['cons']}. Alternatives: {', '.join(om['alternatives'])}.", "",
          "## Investment (12 months, indicative)", f"- Foundations: ${r['investment']['foundations_usd']:,}",
          f"- Initiatives: ${r['investment']['initiatives_usd'][0]:,} – ${r['investment']['initiatives_usd'][1]:,}",
          f"- Total: ${r['investment']['total_12m_usd'][0]:,} – ${r['investment']['total_12m_usd'][1]:,}",
          f"- Estimated annual benefit: ${r['investment']['annual_benefit_usd']:,}", "", "## KPI framework", "**Portfolio:** " + "; ".join(r["kpis"]["portfolio"])]
    L += [f"- **{k}:** {', '.join(v)}" for k, v in r["kpis"]["by_initiative"].items()]
    L += ["", "## Risks & dependencies"] + [f"- {x}" for x in r["risks"]] + ["", "---", "*uniAIverse — AI Strategy, Consulting, Data & MLOps.*"]
    return "\n".join(L)

def to_pdf(r: dict, path: Path) -> Path:
    d = Doc(f"AI Strategy & Roadmap — {r['organisation']}", f"{r['industry']} · {r['staff']} staff")
    d.p(f"<b>Ambition:</b> {r['ambition'] or '—'}").h2("Executive summary").p(r["narrative"])
    d.h2("Prioritised use-case backlog").table([["#", "Use case", "Function", "V/F/R", "Effort", "Score", "Quadrant", "Horizon"]] +
        [[str(b["rank"]), b["name"], b["function"], f"{b['value']}/{b['feasibility']}/{b['risk']}", b["effort"], str(b["score"]), b["quadrant_title"], b["horizon"]] for b in r["backlog"]],
        [8, 48, 24, 16, 16, 14, 24, 28])
    d.h2("Business cases").table([["Use case", "Build USD", "Run/month", "Weeks", "Annual benefit", "Year-1 net", "Payback (mo)"]] +
        [[b["name"], f"{b['business_case']['build_usd'][0]:,}–{b['business_case']['build_usd'][1]:,}", f"{b['business_case']['run_usd_month'][0]:,}–{b['business_case']['run_usd_month'][1]:,}",
          f"{b['business_case']['weeks'][0]}–{b['business_case']['weeks'][1]}", f"{b['business_case']['annual_benefit_usd']:,}", f"{b['business_case']['year1_net_usd']:,}", str(b['business_case']['payback_months'])] for b in r["backlog"]],
        [46, 30, 26, 16, 26, 22, 20])
    d.p("Benefits without a client estimate use the uniAIverse heuristic by value score and must be validated in discovery.", small=True)
    if r["foundations"]:
        d.h2("Foundations required first")
        for f in r["foundations"]: d.h3(f"{f['title']}  (readiness domain: {f['domain']})").bullets(f["actions"])
    d.page().h2("Roadmap")
    for ph in r["phases"]: d.h3(f"Phase {ph['id']} — {ph['title']} (months {ph['months']})").p(ph["goal"], small=True).bullets(ph["items"])
    om = r["operating_model"]
    d.h2("Operating model").p(f"<b>Recommended: {om['title']}</b> — fits {om['fits']}. Pros: {om['pros']}. Cons: {om['cons']}.")
    inv = r["investment"]
    d.h2("Investment — 12 months, indicative").table([["Item", "USD"], ["Foundations", f"{inv['foundations_usd']:,}"], ["Initiatives", f"{inv['initiatives_usd'][0]:,} – {inv['initiatives_usd'][1]:,}"],
        ["Total", f"{inv['total_12m_usd'][0]:,} – {inv['total_12m_usd'][1]:,}"], ["Estimated annual benefit", f"{inv['annual_benefit_usd']:,}"]], [80, 60])
    d.h2("KPI framework").p("<b>Portfolio:</b> " + "; ".join(r["kpis"]["portfolio"]))
    d.bullets([f"<b>{k}:</b> {', '.join(v)}" for k, v in r["kpis"]["by_initiative"].items()])
    d.h2("Risks & dependencies").bullets(r["risks"] or ["None identified"])
    return d.build(path)
