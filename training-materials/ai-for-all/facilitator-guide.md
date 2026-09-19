# Facilitator Guide — AI for All (4 hours)

Materials: `slides/slides.md` (→ `slides/build.sh`), `demos/`, `exercises.md`, glossary handout, five-rules card. The Quest quiz (AI Basics) is the assessment.

| Time | Slide | Segment | What you do and say |
|---|---|---|---|
| 00:00 | 1 | Welcome | "By the end you will use AI at work better than most people who use it daily — and you'll know when not to trust it." |
| 00:05 | 2 | 10-minute win | Everyone does one real task. Walk the room. Ask two people to read their before/after. |
| 00:20 | 3 | The new colleague | Tell it as a story, slowly. Ask: "What would you do with this colleague?" Someone will say "give them the documents." That's the whole course. |
| 00:30 | 4 | How it works | Phone autocomplete on screen. **Run `python demos/01_confident_wrong.py`** — pause on the invented answer. Then show the grounded version. "Same tool. Only the desk changed." |
| 00:50 | 5 | Good at / bad at | Exercise: 20 task cards, tables sort into AI-suitable / not. Discuss the ones they argue about (usually "calculate" and "decide"). |
| 01:10 | | Break | |
| 01:25 | 6–7 | Prompting | **Run `python demos/02_prompt_before_after.py`** on a document from the room. Before/after on screen. Then the folklore slide — let them laugh at "I'll tip you $200". |
| 01:55 | 8 | Data rules | Tell the salary-leak story: a helpful assistant that answered "what does the CEO earn?" because HR files were in the library. Then the table. Point at the company account. |
| 02:15 | 9 | Verify | The three questions. Ask each table for a time AI output was wrong and nobody noticed. |
| 02:30 | | Break | |
| 02:45 | 10 | **Lab** | 45 min. One weekly task per person. Prompt with audience/format/length. Run, check, fix, save. Two volunteers show theirs. |
| 03:30 | 11 | Five rules | Say them, then have the room say them back. Hand out the card. |
| 03:40 | 12 | Quiz | uniAI Quest → AI Basics, 15 questions. Certificate "AI Aware" at ≥ 70%. |
| 03:55 | | Close | "Show one colleague what you built this week. Real users ask things you'd never predict." |

**What goes wrong:** people paste confidential data in the lab — say the rule *before* the lab starts. Engineers get bored — give them the glossary and ask them to explain hallucination to their table in one sentence.
