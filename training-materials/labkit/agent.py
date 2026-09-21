"""A small, readable agent runtime: typed tools, a THINK→ACT→OBSERVE loop, six safety caps, memory tiers, trajectory log.
OFFLINE the 'brain' is a scripted policy (a list of intended steps) so the room sees the machinery; LIVE it can ask a model to choose."""
from __future__ import annotations
import json, time
from dataclasses import dataclass, field
from common import tokens, cost

@dataclass
class Tool:
    name: str; description: str; params: dict; fn: callable; destructive: bool = False; scope: str = "read"
    def schema(self) -> dict: return {"name": self.name, "description": self.description, "input_schema": {"type": "object", "properties": self.params, "required": list(self.params)}}
    def schema_tokens(self) -> int: return tokens(json.dumps(self.schema()))

@dataclass
class Caps:
    max_steps: int = 6; max_cost: float = 0.05; loop_window: int = 2; require_approval: bool = True; allowed_scopes: tuple = ("read", "write"); timeout_s: float = 20

@dataclass
class Run:
    steps: list = field(default_factory=list); cost: float = 0.0; stopped: str = ""; answer: str = ""
    def tool_calls(self): return [(s["tool"], s["args"]) for s in self.steps if s.get("tool")]

def validate_args(tool: Tool, args: dict) -> str | None:
    for k, spec in tool.params.items():
        if k not in args: return f"missing argument '{k}'"
        t = spec.get("type")
        if t == "number" and not isinstance(args[k], (int, float)): return f"'{k}' must be a number"
        if t == "string" and not isinstance(args[k], str): return f"'{k}' must be a string"
        if "enum" in spec and args[k] not in spec["enum"]: return f"'{k}' must be one of {spec['enum']}"
    extra = set(args) - set(tool.params)
    return f"unexpected argument(s) {sorted(extra)}" if extra else None

def run_agent(goal: str, tools: list[Tool], policy, caps: Caps = Caps(), approve=lambda tool, args: True, verbose: bool = True, tier: str = "mid") -> Run:
    """policy(goal, history) -> {'think': str, 'tool': name|None, 'args': {...}, 'answer': str|None}"""
    reg = {t.name: t for t in tools}; run = Run(); t0 = time.time(); sys_tok = 400 + sum(t.schema_tokens() for t in tools); hist_tok = 0
    def log(*a):
        if verbose: print(*a)
    while True:
        if len(run.steps) >= caps.max_steps: run.stopped = f"step cap ({caps.max_steps})"; break
        if run.cost >= caps.max_cost: run.stopped = f"cost cap (${caps.max_cost:.2f})"; break
        if time.time() - t0 > caps.timeout_s: run.stopped = "time cap"; break
        d = policy(goal, run.steps); run.cost += cost(sys_tok + hist_tok + tokens(goal), 120, tier)
        log(f"  THINK  {d.get('think', '')}")
        if d.get("answer") is not None: run.answer = d["answer"]; run.stopped = "answered"; break
        name, args = d.get("tool"), d.get("args", {}); rec = {"think": d.get("think", ""), "tool": name, "args": args}
        recent = [(s["tool"], json.dumps(s["args"], sort_keys=True)) for s in run.steps[-caps.loop_window:]]
        if len(recent) == caps.loop_window and all(r == (name, json.dumps(args, sort_keys=True)) for r in recent):
            run.stopped = "loop detected (same call repeated)"; break
        if name not in reg: rec["obs"] = f"ERROR unknown tool '{name}'"; rec["error"] = True
        else:
            tool = reg[name]; bad = validate_args(tool, args)
            if tool.scope not in caps.allowed_scopes: rec["obs"] = f"BLOCKED scope '{tool.scope}' not permitted"; rec["blocked"] = True
            elif bad: rec["obs"] = f"ERROR {bad}"; rec["error"] = True
            elif tool.destructive and caps.require_approval and not approve(tool, args): rec["obs"] = "BLOCKED human did not approve"; rec["blocked"] = True
            else:
                if tool.destructive and caps.require_approval: log(f"  GATE   human approved {name}({args})")
                try: rec["obs"] = str(tool.fn(**args))
                except Exception as e: rec["obs"] = f"ERROR {e}"; rec["error"] = True
        log(f"  ACT    {name}({', '.join(f'{k}={v!r}' for k, v in args.items())})"); log(f"  OBS    {rec['obs'][:160]}")
        hist_tok += tokens(rec["obs"]) + 40; run.steps.append(rec)
    log(f"  STOP   {run.stopped} · {len(run.steps)} step(s) · ${run.cost:.4f}")
    return run

def scripted(plan: list[dict]):
    """Offline policy: follow a plan, one entry per turn; entries may be callables(history) for branching."""
    def policy(goal, history):
        i = len(history)
        if i >= len(plan): return plan[-1]
        p = plan[i]; return p(history) if callable(p) else p
    return policy

class Memory:
    """Four tiers: short-term (this turn window) · working (scratchpad) · long-term (facts, searchable) · episodic (what happened before)."""
    def __init__(self, window: int = 4): self.window, self.short, self.working, self.long, self.episodes = window, [], {}, [], []
    def add_turn(self, role, text):
        self.short.append((role, text))
        if len(self.short) > self.window:
            old = self.short.pop(0); self.episodes.append(f"{old[0]}: {old[1][:80]}")
    def remember(self, fact: str, tags=()): self.long.append({"fact": fact, "tags": set(tags)})
    def recall(self, query: str, k: int = 2):
        from common import _terms
        q = set(_terms(query)); sc = sorted(((len(q & set(_terms(m["fact"]))) + 2 * len(q & m["tags"]), m["fact"]) for m in self.long), reverse=True)
        return [f for s, f in sc[:k] if s > 0]
    def context_tokens(self) -> int: return sum(tokens(t) for _, t in self.short) + sum(tokens(str(v)) for v in self.working.values())

def trajectory_score(run: Run, expected_tools: list[str], forbidden: list[str] = (), max_steps: int | None = None, must_contain: str = "") -> dict:
    called = [t for t, _ in run.tool_calls()]
    return {"tool_recall": len([t for t in expected_tools if t in called]) / (len(expected_tools) or 1), "order_ok": [t for t in called if t in expected_tools][:len(expected_tools)] == expected_tools,
            "no_forbidden": not any(t in called for t in forbidden), "efficient": (len(run.steps) <= max_steps) if max_steps else True,
            "answer_ok": must_contain.lower() in run.answer.lower() if must_contain else True, "cost": run.cost, "steps": len(run.steps)}
