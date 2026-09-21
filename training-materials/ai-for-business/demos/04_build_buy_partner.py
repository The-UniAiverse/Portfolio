"""AI for Business Leaders · Demo 4 — Build, buy or partner: 3-year TCO and the exit cost (10 min) · Module 5
Shows: total cost of ownership for build vs buy over three years, the break-even user count and a lock-in check
Lab: Put your own numbers in BUILD and BUY. At how many users does the answer flip? What is your exit cost if the vendor doubles the price?
Run: python 04_build_buy_partner.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Business Leaders · Demo 4 — Build, buy or partner: 3-year TCO and the exit cost")
BUILD = {"initial": 60000, "team_per_year": 45000, "infra_per_year": 9000}; BUY = {"setup": 5000, "integration": 12000, "licence_per_user_year": 360, "users": 150, "exit_cost": 15000}
r = biz.tco_build_buy(3, BUILD, BUY); table(["Option", "3-year TCO"], [["Build", money(r["build"])], ["Buy", money(r["buy"])]]); print(f"\n  Cheaper: {r['cheaper'].upper()} by {money(r['difference'])}")
hr(); print("Break-even by number of users:")
for u in (50, 150, 300, 500, 800):
    x = biz.tco_build_buy(3, BUILD, {**BUY, "users": u}); print(f"  {u:>4} users  build {money(x['build']):>9}  buy {money(x['buy']):>9}  → {x['cheaper']}")
hr(); x = biz.tco_build_buy(3, BUILD, {**BUY, "licence_per_user_year": 720}); print(f"If the vendor doubles the price in year 1: buy = {money(x['buy'])} → {x['cheaper']}")
print("\nLock-in checklist: can we export our data and prompts? · is the model swappable? · who owns fine-tunes? · notice period · price-rise cap in the contract")
say("Buy the commodity, build the difference, and price the exit before you sign.")
