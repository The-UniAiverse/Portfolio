"""uniAIverse lab kit — the shared toolkit behind every course demo.

One import gives a demo everything it needs:
    import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *

Design rules (same as the Agentic AI workshop):
  • every demo runs OFFLINE, deterministically, with no API key and no extra packages (pure Python);
  • with an LLM key in the repo's .env the same demo calls a real model where that teaches more;
  • every demo ends with a 'Say it:' line — the trainer's closing sentence.
Modules: core (printing) · ml (models from scratch) · dataq (data quality, PII, drift) · evals (metrics, judges, gates)
         · agent (tool loop with caps) · guard (security controls) · ops (registry, gateway, SLOs) · biz (ROI, scoring) · text (extraction, voice, claims)
"""
import sys as _sys, pathlib as _pl
_WS = _pl.Path(__file__).resolve().parents[1] / "agentic-ai-workshop" / "demos"
if str(_WS) not in _sys.path: _sys.path.insert(0, str(_WS))
from common import *                      # noqa: F401,F403  banner, tokens, cost, RATES, load_docs, chunkers, bm25, semantic, rrf, rerank, answer, hr, llm, LIVE
from common import _terms                 # noqa: F401
from .core import *                       # noqa: F401,F403
from . import ml, dataq, evals, agent, guard, ops, biz, text   # noqa: F401
