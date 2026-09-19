# Card 4 — My bot gave a wrong answer. What do I do?
**Step 1 — Look at what it fetched.** Your tool shows this. Find it.
Was the right information in there?
**NO → library problem.** Is the document in the library? Did it read the file properly (check extracted text)? Are the chunks cut badly (read five)? Is hybrid search on? Is reranking on?
**YES → answering problem.** Sending too many chunks (try fewer)? Grounding instruction present? Two documents contradicting? Is the chunk itself wrong or out of date?
Most people start by rewriting the instructions. Most problems are in the library.
