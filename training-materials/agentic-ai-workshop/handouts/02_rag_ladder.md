# Card 2 — The RAG ladder
| Level | Adds | You need it when | Cost/speed |
|---|---|---|---|
| Basic | fetch → answer | clean FAQ over tidy documents | 1× |
| Advanced | query rewriting · hybrid search · reranking · contextual chunks | real company documents — where most systems should live | 1.1× |
| Hybrid | several stores + a router (documents / SQL / live APIs) | you have documents AND a database AND live systems | 1.3× |
| Agentic | the model decides what to look up, checks, retries | multi-step, cross-system questions | 5–10×, 10× slower |
Earn your way up. An agent does not repair bad retrieval — it repeats it. Go up only when you hit a wall you can name.
Settings to start: chunk 500 words by heading · overlap 10–15% · contextual prefix ON · hybrid ON · rerank ON · fetch 50 keep 5 · temperature 0–0.2.
