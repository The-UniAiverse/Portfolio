"""Dry-run every demo before a delivery (≈20 s offline):  python run_all.py
Any failure prints here — fix it before the room does. Add a demo: drop NN_name.py in this folder; it runs in order."""
import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent
runs = [[f.name] for f in sorted(HERE.glob("[0-9][0-9]_*.py"))] + [["05_agent.py", "--runaway"], ["05_agent.py", "--inject"]]
for args in runs:
    print(f"\n>>> python {' '.join(args)}")
    r = subprocess.run([sys.executable, *args], cwd=HERE, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    print(r.stdout[-1200:])
    if r.returncode: print(r.stderr[-800:]); sys.exit(f"FAILED: {' '.join(args)}")
print("\nALL DEMOS OK")
