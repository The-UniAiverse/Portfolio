# Card 1 — The cost of one question
**Input tokens** = system prompt + retrieved chunks (k × ~500) + conversation history + question
**Output tokens** = the answer (+ reasoning tokens, if enabled)
**Cost** = input ÷ 1,000,000 × input rate + output ÷ 1,000,000 × output rate
**Monthly** = cost × questions/day × 30
Rules of thumb: 1 token ≈ ¾ word · 1 page ≈ 700 tokens · output ≈ 5× input price · cached prefix ≈ 90% off · non-English 2–5× tokens
The two explosions: untrimmed history (×10–30 by message 40) · flagship-for-everything (×5).
Fix: trim/summarise history after ~10 messages · mid-tier for grounded answering · cache the static prefix · cap answer length.
