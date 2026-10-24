"""LLM cost calculator — run: python cost_calculator.py
Edit RATES as prices change (per 1M tokens, USD)."""
RATES = {  # verify quarterly
    "cheap":    {"in": 0.25, "out": 1.25, "cached_in": 0.03},
    "mid":      {"in": 3.00, "out": 15.00, "cached_in": 0.30},
    "flagship": {"in": 15.00, "out": 75.00, "cached_in": 1.50},
}

def per_request(tier, system_tokens, context_tokens, history_tokens, question_tokens, answer_tokens, cache_system=True):
    r = RATES[tier]
    sys_cost = system_tokens / 1e6 * (r["cached_in"] if cache_system else r["in"])
    dyn_in = (context_tokens + history_tokens + question_tokens) / 1e6 * r["in"]
    out = answer_tokens / 1e6 * r["out"]
    return sys_cost + dyn_in + out

def monthly(cost_per_request, requests_per_day, days=30):
    return cost_per_request * requests_per_day * days

if __name__ == "__main__":
    scenarios = {
        "FAQ bot (no RAG)":        dict(tier="cheap", system_tokens=800, context_tokens=0,    history_tokens=500,  question_tokens=80,  answer_tokens=200),
        "RAG assistant (k=5)":     dict(tier="mid",   system_tokens=1000, context_tokens=2500, history_tokens=1500, question_tokens=100, answer_tokens=400),
        "RAG, history untrimmed":  dict(tier="mid",   system_tokens=1000, context_tokens=2500, history_tokens=30000, question_tokens=100, answer_tokens=400),
        "Agentic (6 steps ≈ 30×)": dict(tier="mid",   system_tokens=6000, context_tokens=30000, history_tokens=6000, question_tokens=100, answer_tokens=4000),
    }
    for name, s in scenarios.items():
        c = per_request(**s)
        print(f"{name:26s} ${c:.4f}/req   {monthly(c, 100):8.0f} $/mo @100/day   {monthly(c, 1000):8.0f} $/mo @1000/day")
