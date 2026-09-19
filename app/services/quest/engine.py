"""uniAI Quest engine: quizzes, scoring, XP, tiers, interview challenges."""
from __future__ import annotations
import hashlib, random
from datetime import date
from pathlib import Path
import yaml
from app.core import db

HERE = Path(__file__).parent

def bank() -> dict: return yaml.safe_load((HERE / "question_bank.yaml").read_text())
def tiers() -> dict: return yaml.safe_load((HERE / "quest_tiers.yaml").read_text())

def tier_of(user_id: str) -> str:
    return (db.get_user(user_id) or {}).get("tier", "free")

def entitlements(tier: str) -> dict:
    t = tiers()["tiers"]
    return t.get(tier, t["free"])

def level_for(xp: int) -> dict:
    lv = tiers()["levels"]; cur = lv[0]; nxt = None
    for i, l in enumerate(lv):
        if xp >= l["xp"]:
            cur = l; nxt = lv[i + 1] if i + 1 < len(lv) else None
    return {"title": cur["title"], "xp": xp, "next": nxt}

def quizzes_today(user_id: str) -> int:
    start = date.today().toordinal()
    with db.conn() as c:
        rows = c.execute("SELECT created_at FROM quiz_attempts WHERE user_id=? AND kind='quiz'", (user_id,)).fetchall()
    return sum(1 for r in rows if date.fromtimestamp(r["created_at"]).toordinal() == start)

def topics_for(tier: str) -> list[dict]:
    ent = entitlements(tier); b = bank()
    allowed = None if ent["topics"] == "all" else set(ent["topics"])
    return [{"id": t["id"], "title": t["title"], "emoji": t["emoji"], "blurb": t["blurb"],
             "questions": len(t["questions"]), "locked": allowed is not None and t["id"] not in allowed}
            for t in b["topics"]]

def _qid(topic: str, q: dict) -> str:
    return hashlib.sha1(f"{topic}|{q['q']}".encode()).hexdigest()[:10]

def build_quiz(user_id: str, topic: str, n: int = 5, difficulty: int | None = None) -> dict:
    tier = tier_of(user_id); ent = entitlements(tier)
    if ent["topics"] != "all" and topic not in ent["topics"]:
        raise PermissionError(f"Topic '{topic}' needs Bronze or above.")
    if quizzes_today(user_id) >= ent["quizzes_per_day"]:
        raise PermissionError(f"Daily limit reached for the {ent['title']} tier ({ent['quizzes_per_day']} quizzes/day). Come back tomorrow or upgrade.")
    t = next((x for x in bank()["topics"] if x["id"] == topic), None)
    if not t: raise KeyError("unknown topic")
    maxd = min(ent["max_difficulty"], difficulty or ent["max_difficulty"])
    pool = [q for q in t["questions"] if q["d"] <= maxd]
    random.shuffle(pool); picked = pool[:n]
    return {"topic": t["id"], "title": t["title"], "emoji": t["emoji"], "tier": tier, "max_difficulty": maxd,
            "questions": [{"id": _qid(t["id"], q), "d": q["d"], "q": q["q"], "options": q["options"], "tags": q["tags"]} for q in picked],
            "locked_higher_difficulty": ent["max_difficulty"] < 3}

def grade(user_id: str, topic: str, answers: dict[str, int]) -> dict:
    t = next((x for x in bank()["topics"] if x["id"] == topic), None)
    if not t: raise KeyError("unknown topic")
    rules = tiers()["xp_rules"]; by_id = {_qid(t["id"], q): q for q in t["questions"]}
    results, xp, correct = [], 0, 0
    for qid, a in answers.items():
        q = by_id.get(qid)
        if not q: continue
        ok = int(a) == q["answer"]; correct += ok
        if ok: xp += rules["correct"][q["d"]]
        results.append({"id": qid, "correct": ok, "your_answer": a, "answer": q["answer"], "answer_text": q["options"][q["answer"]], "why": q["why"]})
    if results and correct == len(results): xp += rules["perfect_quiz_bonus"]
    db.get_user(user_id)
    with db.conn() as c:
        c.execute("INSERT INTO quiz_attempts (user_id, topic, difficulty, score, total, xp, kind, created_at) VALUES (?,?,?,?,?,?,?,?)",
                  (user_id, topic, max((by_id[r["id"]]["d"] for r in results), default=1), correct, len(results), xp, "quiz", db.now()))
        c.execute("UPDATE users SET xp = xp + ? WHERE id=?", (xp, user_id))
        total_xp = c.execute("SELECT xp FROM users WHERE id=?", (user_id,)).fetchone()["xp"]
    return {"topic": topic, "score": correct, "total": len(results), "xp_earned": xp, "results": results,
            "level": level_for(total_xp), "perfect": bool(results) and correct == len(results)}

def challenges(user_id: str) -> dict:
    tier = tier_of(user_id); ent = entitlements(tier); b = bank()
    items = b["interview_challenges"]
    if not ent["interview_challenges"]:
        return {"tier": tier, "locked": True, "preview": [{"id": c["id"], "topic": c["topic"], "level": c["level"], "prompt": c["prompt"]} for c in items[:2]],
                "unlock": "Interview challenges with model answers are in Silver and above."}
    return {"tier": tier, "locked": False, "challenges": items}

def submit_challenge(user_id: str, challenge_id: str, self_rating: int, notes: str = "") -> dict:
    ent = entitlements(tier_of(user_id))
    if not ent["interview_challenges"]: raise PermissionError("Silver or above required.")
    ch = next((c for c in bank()["interview_challenges"] if c["id"] == challenge_id), None)
    if not ch: raise KeyError("unknown challenge")
    xp = tiers()["xp_rules"]["challenge_submitted"]
    with db.conn() as c:
        c.execute("INSERT INTO quiz_attempts (user_id, topic, difficulty, score, total, xp, kind, created_at) VALUES (?,?,?,?,?,?,?,?)",
                  (user_id, ch["topic"], ch["level"], self_rating, 5, xp, "challenge", db.now()))
        c.execute("UPDATE users SET xp = xp + ? WHERE id=?", (xp, user_id))
        total_xp = c.execute("SELECT xp FROM users WHERE id=?", (user_id,)).fetchone()["xp"]
    return {"challenge": ch, "self_rating": self_rating, "xp_earned": xp, "level": level_for(total_xp),
            "mentor_feedback": "Available in Gold and Platinum — request a session." if ent["mentor_hours_per_month"] == 0 else "Request a session to have this reviewed."}

def progress(user_id: str) -> dict:
    u = db.get_user(user_id); ent = entitlements(u["tier"])
    with db.conn() as c:
        rows = [dict(r) for r in c.execute("SELECT * FROM quiz_attempts WHERE user_id=? ORDER BY created_at DESC LIMIT 100", (user_id,))]
    by_topic: dict[str, dict] = {}
    for r in rows:
        if r["kind"] != "quiz": continue
        d = by_topic.setdefault(r["topic"], {"attempts": 0, "correct": 0, "total": 0})
        d["attempts"] += 1; d["correct"] += r["score"]; d["total"] += r["total"]
    weakest = sorted(((k, v["correct"] / v["total"]) for k, v in by_topic.items() if v["total"]), key=lambda x: x[1])[:2]
    return {"user_id": user_id, "tier": u["tier"], "entitlements": ent, "level": level_for(u["xp"]),
            "quizzes_today": quizzes_today(user_id), "by_topic": by_topic, "recent": rows[:10],
            "suggested_next": [k for k, _ in weakest] or ["ai-basics"],
            "learning_path_hint": "Weak topics map to courses: rag → Build Your Own AI Bot; agents → Agentic AI Engineer; tokens-cost → LLM Cost workshop; ai-ethics → AI Governance."}
