"""AI Productivity Workflows · Demo 4 — Your prompt library — linted (10 min) · Module 4
Shows: five saved prompts checked against the four-part standard (role, input, format, check) with a quality score
Lab: Write five prompts for your own week in data/prompts.yaml format. Aim for 4/4 on each. Share the best one with the room.
Run: python 04_prompt_library.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Productivity Workflows · Demo 4 — Your prompt library — linted")
import yaml
lib = yaml.safe_load(data_path(__file__, "prompts.yaml").read_text())
def lint(p):
    t = p["prompt"].lower(); c = {"role/context": any(w in t for w in ("you are", "for a", "audience", "context")), "input slot": "{" in p["prompt"], "format": any(w in t for w in ("bullet", "table", "words", "headings", "format", "json")),
                                  "check step": any(w in t for w in ("not in", "unsure", "flag", "source", "verify", "do not invent"))}
    return c
rows = []
for p in lib:
    c = lint(p); rows.append([p["name"], *("✓" if v else "·" for v in c.values()), f"{sum(c.values())}/4"])
table(["Prompt", "Role", "Input", "Format", "Check", "Score"], rows)
worst = min(lib, key=lambda p: sum(lint(p).values())); print(f"\nWeakest: '{worst['name']}' → {worst['prompt']!r}\nFix it by adding: " + ", ".join(k for k, v in lint(worst).items() if not v))
say("A saved prompt is a small procedure. If it has no check step, it is not finished.")
