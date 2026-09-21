"""Machine learning from scratch (pure Python) — small enough to read on a projector, real enough to teach with.
Logistic regression, gradient-boosted stumps, metrics, calibration, permutation importance, a leaky-feature trap."""
from __future__ import annotations
import math, random

def make_churn(n: int = 900, seed: int = 7, leak: bool = False, shift: float = 0.0):
    """Synthetic telecom-style churn table. `leak=True` adds a feature that is only known AFTER the outcome.
    `shift` moves the population (older tenure, more tickets) to simulate drift."""
    r = random.Random(seed); X, y = [], []
    names = ["tenure_months", "monthly_bill", "support_tickets", "late_payments", "uses_app", "contract_annual"]
    for _ in range(n):
        tenure = max(1, r.gauss(24 + 10 * shift, 14)); bill = max(10, r.gauss(60, 20)); tickets = max(0, round(r.gauss(1.5 + 2 * shift, 1.5)))
        late = max(0, round(r.gauss(0.8, 1))); app = 1 if r.random() < 0.6 else 0; annual = 1 if r.random() < 0.4 else 0
        z = -1.2 - 0.045 * tenure + 0.018 * bill + 0.55 * tickets + 0.5 * late - 0.7 * app - 1.1 * annual
        p = 1 / (1 + math.exp(-z)); label = 1 if r.random() < p else 0
        row = [tenure, bill, tickets, late, app, annual]
        if leak: row.append(label * r.uniform(0.8, 1.0) + (1 - label) * r.uniform(0, 0.15))   # 'retention_call_made' — recorded after churn
        X.append(row); y.append(label)
    return X, y, names + (["retention_call_made"] if leak else [])

def split(X, y, test: float = 0.3, seed: int = 1):
    idx = list(range(len(X))); random.Random(seed).shuffle(idx); k = int(len(X) * (1 - test))
    tr, te = idx[:k], idx[k:]; return [X[i] for i in tr], [y[i] for i in tr], [X[i] for i in te], [y[i] for i in te]

class Scaler:
    def fit(self, X):
        n = len(X); self.m = [sum(c) / n for c in zip(*X)]; self.s = [math.sqrt(sum((v - m) ** 2 for v in c) / n) or 1 for c, m in zip(zip(*X), self.m)]; return self
    def transform(self, X): return [[(v - m) / s for v, m, s in zip(r, self.m, self.s)] for r in X]

class LogReg:
    """Logistic regression by gradient descent."""
    def __init__(self, lr: float = 0.3, epochs: int = 200): self.lr, self.epochs = lr, epochs
    def fit(self, X, y):
        self.sc = Scaler().fit(X); Z = self.sc.transform(X); d = len(Z[0]); self.w = [0.0] * d; self.b = 0.0; n = len(Z)
        for _ in range(self.epochs):
            gw = [0.0] * d; gb = 0.0
            for r, t in zip(Z, y):
                e = 1 / (1 + math.exp(-(sum(a * b for a, b in zip(self.w, r)) + self.b))) - t
                for j in range(d): gw[j] += e * r[j]
                gb += e
            self.w = [w - self.lr * g / n for w, g in zip(self.w, gw)]; self.b -= self.lr * gb / n
        return self
    def proba(self, X): return [1 / (1 + math.exp(-(sum(a * b for a, b in zip(self.w, r)) + self.b))) for r in self.sc.transform(X)]

class BoostedStumps:
    """Gradient boosting with one-split trees on log-loss — the idea behind XGBoost/LightGBM in 25 lines."""
    def __init__(self, rounds: int = 40, lr: float = 0.3): self.rounds, self.lr = rounds, lr
    def fit(self, X, y):
        p0 = min(max(sum(y) / len(y), 1e-3), 1 - 1e-3); self.f0 = math.log(p0 / (1 - p0)); F = [self.f0] * len(X); self.stumps = []
        cols = list(zip(*X)); cuts = [sorted(set(c))[:: max(1, len(set(c)) // 12)] for c in cols]
        for _ in range(self.rounds):
            g = [t - 1 / (1 + math.exp(-f)) for t, f in zip(y, F)]; best = None
            for j, cs in enumerate(cuts):
                for c in cs:
                    L = [gi for gi, r in zip(g, X) if r[j] <= c]; R = [gi for gi, r in zip(g, X) if r[j] > c]
                    if not L or not R: continue
                    ml_, mr = sum(L) / len(L), sum(R) / len(R); gain = len(L) * ml_ ** 2 + len(R) * mr ** 2
                    if best is None or gain > best[0]: best = (gain, j, c, ml_, mr)
            if best is None: break
            _, j, c, a, b = best; self.stumps.append((j, c, a * 4, b * 4))       # ×4 ≈ Newton step for p≈0.5
            F = [f + self.lr * (a * 4 if r[j] <= c else b * 4) for f, r in zip(F, X)]
        return self
    def proba(self, X):
        out = []
        for r in X:
            f = self.f0 + sum(self.lr * (a if r[j] <= c else b) for j, c, a, b in self.stumps); out.append(1 / (1 + math.exp(-f)))
        return out

def confusion(y, p, thr: float = 0.5):
    tp = sum(1 for t, q in zip(y, p) if t and q >= thr); fp = sum(1 for t, q in zip(y, p) if not t and q >= thr)
    fn = sum(1 for t, q in zip(y, p) if t and q < thr); tn = len(y) - tp - fp - fn; return tp, fp, fn, tn
def metrics(y, p, thr: float = 0.5) -> dict:
    tp, fp, fn, tn = confusion(y, p, thr); pr = tp / (tp + fp) if tp + fp else 0.0; rc = tp / (tp + fn) if tp + fn else 0.0
    return {"accuracy": (tp + tn) / len(y), "precision": pr, "recall": rc, "f1": 2 * pr * rc / (pr + rc) if pr + rc else 0.0, "auc": auc(y, p)}
def auc(y, p) -> float:
    pos = [q for t, q in zip(y, p) if t]; neg = [q for t, q in zip(y, p) if not t]
    if not pos or not neg: return 0.5
    return sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg))
def calibration(y, p, bins: int = 5):
    """[(predicted mean, actual rate, count)] — a calibrated model has the first two equal."""
    out = []
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins; sel = [(t, q) for t, q in zip(y, p) if lo <= q < hi or (b == bins - 1 and q == 1)]
        if sel: out.append((sum(q for _, q in sel) / len(sel), sum(t for t, _ in sel) / len(sel), len(sel)))
    return out
def permutation_importance(model, X, y, names, seed: int = 3):
    base = auc(y, model.proba(X)); r = random.Random(seed); out = []
    for j, nm in enumerate(names):
        col = [row[j] for row in X]; r.shuffle(col); Xp = [row[:j] + [c] + row[j + 1:] for row, c in zip(X, col)]
        out.append((nm, base - auc(y, model.proba(Xp))))
    return sorted(out, key=lambda x: -x[1])
def group_rates(y, p, groups, thr: float = 0.5) -> dict:
    """Selection rate and recall per group — the two numbers a fairness review starts with."""
    out = {}
    for g in sorted(set(groups)):
        idx = [i for i, x in enumerate(groups) if x == g]; sel = sum(1 for i in idx if p[i] >= thr)
        pos = [i for i in idx if y[i]]; out[g] = {"n": len(idx), "selection_rate": sel / len(idx), "recall": sum(1 for i in pos if p[i] >= thr) / len(pos) if pos else 0.0}
    return out
