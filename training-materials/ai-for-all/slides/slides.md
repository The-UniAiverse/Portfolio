---
marp: true
theme: default
paginate: true
style: |
  section { font-family: Georgia, "Iowan Old Style", serif; color: #14213d; background: #fbfaf7; }
  h1, h2 { color: #1f2a44; } strong { color: #0f766e; } table { font-size: 0.85em; }
  section.lead h1 { font-size: 2.4em; } footer { color: #5b6170; font-size: 0.6em; }
footer: "uniAIverse Academy · AI for All · v2.0"
---
<!-- _class: lead -->
# AI for All
## Use AI at work — confidently, safely, and better than most people do
**4 hours · no technical background needed**

---
# The 10-minute win
Open the approved AI tool. Do one of these with something real from your week:
1. Rewrite an email you found hard to write
2. Summarise a long document into five bullet points
3. Turn messy notes into a clean list of actions

*Then tell your neighbour what surprised you.*

---
# The new colleague
Imagine hiring someone brilliant who has read every book and website — and has **never worked here**.

Ask them "what's our refund policy?" and they will answer. Confidently. Beautifully. **And they'll make it up.**

That's an AI model. It isn't lying. It has nothing to go on.

---
# How it actually works
- It's the autocomplete on your phone — trained on most of the internet
- It predicts the next word. Again. And again.
- **There is no database inside.** Nothing is stored or looked up
- It never stops, so when it doesn't know, it produces the most **plausible** answer anyway

> That's called a hallucination. It's the machine doing its job — in a situation where its job is the wrong thing to do.

<!-- DEMO: demos/01_confident_wrong.py -->

---
# Good at · Bad at
| Ask it to… | Don't ask it to… |
|---|---|
| Draft, rewrite, change tone | State facts you can't check |
| Summarise, extract actions | Count, total, calculate |
| Translate, simplify | Tell you what happened this week |
| Brainstorm, structure | Decide for you |
| Explain a concept | Remember last week's chat |

---
# Prompting that works
**Weak:** "Summarise this."

**Strong:**
```
Summarise this for the leadership team.
At most 5 bullets. Each bullet ≤ 15 words.
Highlight any decision that needs a date.
Keep the numbers exactly as written.
```
Give it: **who it's for · the format · the length · an example if you have one.**

<!-- DEMO: demos/02_prompt_before_after.py -->

---
# Things that don't work
- "Please" and "thank you" — costs money at scale, changes nothing
- "I'll tip you $200" — no
- "You'll be penalised if wrong" — no
- "Be thorough but brief" — contradiction. Pick one and give a number
- "Don't be verbose" → weak. "Answer in three sentences" → strong

---
# Data: what may and may not go in
| Never paste | Fine to paste |
|---|---|
| Customer personal data | Public documents |
| Employee records, salaries | Your own drafts |
| Unpublished financials | Meeting notes without names |
| Confidential contracts | Generic questions |
| Passwords, keys | Anything already public |

Use the **company** account. Never a personal one for company work.

---
# Verify before you rely
1. Does it cite a source you can open?
2. Are the numbers the same as the original?
3. Would you sign your name under it?

*The person who says "the AI wrote it, it's probably fine" becomes a risk. The person who says "I checked three things and one was wrong" becomes more valuable.*

---
# Lab · Automate one weekly task
1. Pick a task you do every week that involves reading or writing (15 min)
2. Write the prompt with audience, format, length (10 min)
3. Run it on real material. Check it. Fix the prompt. (15 min)
4. Save it. Show one neighbour. (5 min)

---
# The five rules
1. **Verify** facts and numbers before you use them
2. **Never** paste confidential data into AI tools
3. **Say the format** you want — length, audience, structure
4. **Give context** — the AI knows nothing about your company
5. **You own the output.** Not the tool.

---
<!-- _class: lead -->
# Quiz · 15 questions
uniAI Quest → AI Basics · Then keep playing at home.
