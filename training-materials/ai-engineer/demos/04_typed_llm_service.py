"""AI Engineer · Demo 4 — LLM APIs for engineers: structured output, validation, retries (25 min) · Module 4
Shows: a typed extraction service: JSON schema, validation, repair-and-retry on malformed output, exponential backoff on rate limits, and a test suite that runs without the network
Lab: Add a field to the schema and a test for it. Then make the fake model return a wrong type and confirm your service repairs or rejects it — never passes it on.
Run: python 04_typed_llm_service.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Engineer · Demo 4 — LLM APIs for engineers: structured output, validation, retries")
import json, itertools
SCHEMA = {"invoice_no": str, "total": float, "currency": str, "due_date": str}
class FakeLLM:
    """Stands in for the provider so tests are deterministic: returns a scripted sequence of failures and outputs."""
    def __init__(self, script): self.script = iter(script); self.calls = 0
    def __call__(self, prompt):
        self.calls += 1; r = next(self.script)
        if isinstance(r, Exception): raise r
        return r
class RateLimit(Exception): pass
def validate(raw):
    try: obj = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    except ValueError: return None, "not JSON"
    for k, t in SCHEMA.items():
        if k not in obj: return None, f"missing '{k}'"
        if t is float and isinstance(obj[k], str):
            try: obj[k] = float(obj[k].replace(",", ""))
            except ValueError: return None, f"'{k}' not a number"
        if not isinstance(obj[k], t): return None, f"'{k}' wrong type"
    return obj, None
def extract(text_, model, max_tries=4):
    prompt = f"Return ONLY JSON with keys {list(SCHEMA)}.\n{text_}"; delay = 0.5
    for attempt in range(1, max_tries + 1):
        try: raw = model(prompt)
        except RateLimit: print(f"    try {attempt}: 429 rate limited → backoff {delay:.1f}s"); delay *= 2; continue
        obj, err = validate(raw)
        if obj: print(f"    try {attempt}: valid"); return obj
        print(f"    try {attempt}: invalid ({err}) → re-ask with the error message"); prompt += f"\nYour last answer was invalid: {err}. Return only valid JSON."
    raise ValueError("gave up after retries — route to human queue")
GOOD = '{"invoice_no": "INV-2291", "total": 48250.0, "currency": "INR", "due_date": "2026-10-15"}'
CASES = {"clean first time": [GOOD], "chatty wrapper + string number": ['Sure! Here you go:\n{"invoice_no": "INV-2291", "total": "48,250.00", "currency": "INR", "due_date": "2026-10-15"}'], "rate limit, then missing field, then good": [RateLimit(), '{"invoice_no": "INV-2291"}', GOOD], "never valid": ["I cannot", "nope", "{}", "{"]}
passed = 0
for name, script in CASES.items():
    print(f"\n  TEST {name}"); m = FakeLLM(script)
    try: out = extract("Invoice INV-2291 … total INR 48,250.00 due 15 Oct 2026", m); ok = out["total"] == 48250.0
    except ValueError as e: ok = name == "never valid"; print(f"    → {e}")
    passed += ok; print(f"    {'PASS' if ok else 'FAIL'} · model calls {m.calls}")
print(f"\n{passed}/{len(CASES)} tests passed — no network, no API key, runs in CI.")
say("Treat the model like any flaky upstream service: schema at the door, retries with backoff, and a human queue for what is left.")
