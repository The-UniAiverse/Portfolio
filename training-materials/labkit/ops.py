"""MLOps / LLMOps building blocks: a model registry with promotion and rollback, a versioned RAG stack manifest,
a model gateway (routing, caching, budgets, cost attribution) and SLO burn alerts."""
from __future__ import annotations
import hashlib, json
from common import tokens, RATES

class Registry:
    STAGES = ["candidate", "staging", "production", "archived"]
    def __init__(self): self.versions, self.log = {}, []
    def register(self, name, version, metrics: dict, artefact: str = "", card: dict | None = None):
        self.versions[(name, version)] = {"stage": "candidate", "metrics": metrics, "hash": hashlib.sha256(artefact.encode()).hexdigest()[:10], "card": card or {}}; self.log.append(f"register {name}:{version}")
    def production(self, name): return next((v for (n, v), m in self.versions.items() if n == name and m["stage"] == "production"), None)
    def promote(self, name, version, gates: dict) -> tuple[bool, list[str]]:
        """Promotion is a decision with evidence: every gate is (metric, floor). Missing model card blocks production."""
        m = self.versions[(name, version)]; fails = [f"{k} {m['metrics'].get(k, 0):.3f} < {v}" for k, v in gates.items() if m["metrics"].get(k, 0) < v]
        if not m["card"].get("intended_use"): fails.append("model card missing 'intended_use'")
        cur = self.production(name)
        if cur and m["metrics"].get("auc", 0) < self.versions[(name, cur)]["metrics"].get("auc", 0) - 0.01: fails.append(f"worse than production {cur}")
        if fails: self.log.append(f"REJECT {name}:{version} — {'; '.join(fails)}"); return False, fails
        if cur: self.versions[(name, cur)]["stage"] = "archived"; self.previous = cur
        m["stage"] = "production"; self.log.append(f"promote {name}:{version} → production"); return True, []
    def rollback(self, name):
        cur = self.production(name); prev = getattr(self, "previous", None)
        if not prev: return None
        self.versions[(name, cur)]["stage"] = "archived"; self.versions[(name, prev)]["stage"] = "production"; self.log.append(f"ROLLBACK {name}: {cur} → {prev}"); return prev

def canary(old_p: list[float], new_p: list[float], y: list[int], share: float = 0.1) -> dict:
    """Blue/green with a canary slice: compare error on the same traffic before switching everyone."""
    k = max(1, int(len(y) * share)); err = lambda p: sum(abs((q >= 0.5) - t) for q, t in zip(p[:k], y[:k])) / k
    return {"canary_rows": k, "old_error": err(old_p), "new_error": err(new_p), "switch": err(new_p) <= err(old_p) * 1.05}

def stack_manifest(prompt: str, embedding_model: str, chunking: dict, index_docs: list[str], llm_model: str) -> dict:
    """Everything that changes a RAG answer, pinned and hashed. If the hash changes, re-run the evals."""
    parts = {"prompt": hashlib.sha256(prompt.encode()).hexdigest()[:8], "embedding_model": embedding_model, "chunking": chunking,
             "index": hashlib.sha256("".join(sorted(index_docs)).encode()).hexdigest()[:8], "llm_model": llm_model}
    parts["stack_version"] = hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest()[:10]; return parts
def diff_manifest(a: dict, b: dict) -> list[str]: return [f"{k}: {a[k]} → {b[k]}" for k in a if k != "stack_version" and a[k] != b[k]]

class Gateway:
    """One door to every model: route by difficulty, cache repeats, enforce team budgets, attribute cost."""
    def __init__(self, budgets: dict[str, float]): self.budgets, self.spend, self.cache, self.rows = budgets, {k: 0.0 for k in budgets}, {}, []
    @staticmethod
    def difficulty(q: str) -> str:
        ql = q.lower()
        if any(w in ql for w in ("compare", "plan", "why", "analyse", "analyze", "multi", "step")) or len(q.split()) > 40: return "flagship"
        if any(w in ql for w in ("summar", "explain", "draft", "extract")) or len(q.split()) > 12: return "mid"
        return "cheap"
    def call(self, team: str, q: str, out_tokens: int = 200) -> dict:
        key = hashlib.md5(q.strip().lower().encode()).hexdigest()
        if key in self.cache: row = {"team": team, "tier": "cache", "cost": 0.0, "status": "cache hit"}
        else:
            tier = self.difficulty(q); i, o = RATES[tier]; c = tokens(q) / 1e6 * i + out_tokens / 1e6 * o
            if self.spend[team] + c > self.budgets[team]: row = {"team": team, "tier": tier, "cost": 0.0, "status": "BLOCKED budget"}
            else: self.spend[team] += c; self.cache[key] = True; row = {"team": team, "tier": tier, "cost": c, "status": "ok"}
        self.rows.append(row); return row
    def report(self) -> list[list]:
        return [[t, sum(1 for r in self.rows if r["team"] == t), sum(1 for r in self.rows if r["team"] == t and r["tier"] == "cache"), f"${self.spend[t]:.4f}", f"${self.budgets[t]:.4f}",
                 sum(1 for r in self.rows if r["team"] == t and "BLOCKED" in r["status"])] for t in self.budgets]

def slo_burn(good: int, total: int, target: float = 0.99, window_share: float = 1 / 30) -> dict:
    """Error-budget burn rate: 1.0 = spending the month's budget exactly on schedule; >2 page someone."""
    err = 1 - good / total if total else 0.0; budget = 1 - target; burn = err / budget if budget else 0.0
    return {"availability": good / total if total else 1.0, "burn_rate": burn, "action": "PAGE" if burn >= 14 else "TICKET" if burn >= 2 else "ok", "budget_left": max(0.0, 1 - burn * window_share)}
