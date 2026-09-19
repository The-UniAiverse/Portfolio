"""AI for All · Demo 2 — weak prompt vs strong prompt on the same document (5 min).
Run: python demos/02_prompt_before_after.py [path/to/document.txt]"""
import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "agentic-ai-workshop" / "demos"))
from common import *
banner("AI for All · Demo 2 — prompting that works")
doc = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else load_docs()[1]["text"]
weak = "Summarise this."
strong = ("Summarise this for a customer-service team lead. At most 5 bullets, each under 15 words. "
          "Keep every number and time limit exactly as written. End with the single rule most often broken.")
for label, p in [("WEAK", weak), ("STRONG", strong)]:
    print(f"\n{label} prompt: {p}\n")
    if LIVE: print("   " + (llm.complete(f"{p}\n\n{doc}", max_tokens=250) or "").replace("\n", "\n   "))
    elif label == "WEAK": print("   The document describes Acme's refund and claims policy, covering late deliveries, damaged goods, lost shipments and exclusions, and explains how customers can make claims…  ← vague, no numbers, no use")
    else: print("   • Late >24h → shipping fee refunded within 7 working days; claim within 14 days\n   • Damage: photos + packing slip within 48h; up to INR 50,000\n   • Claims >INR 10,000 go to the weekly Claims Committee\n   • Lost = not delivered within 10 working days; full refund\n   • No refund for wrong address, force majeure, customs holds\n   Most broken rule: the 48-hour photo deadline")
print("\nSay it: 'The strong prompt is longer. That's fine. Clear beats short.'")
