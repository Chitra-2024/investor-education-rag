# Error analysis

Failures are from the retrieval evaluation on the 25-question gold set.
Chunk size 800, k=5, unless stated.

## 1. Q10: "Who is not allowed to invest in the Choice Overnight Fund?"
- **What happened:** The chunk with the answer (p.48) ranked 7th of 407, just outside the top 5.
  The top result (score 0.712) was the due-diligence boilerplate on p.67, and the evidence chunk scored 0.542.
- **Category:** retrieval miss
- **Root cause:** The question contains the fund name, and many boilerplate chunks repeat
  "Choice Overnight Fund", so they scored higher than the chunk that answers the question.
  Supporting test: with the fund name removed from the question, the evidence chunk moved to rank 2.
- **Fix tried:** (fill in after the sentence-chunking results)

## 2. Q13: "How much money does the Choice Overnight Fund aim to collect at minimum during its NFO?"
- **What happened:** The chunk with "seeks to collect Rs. 20 crores" (p.42) ranked 14th of 407.
  The chunk just before it ended with the heading "Minimum Target amount" but without the figure,
  so heading and value ended up in two different chunks. The top results were other
  "Minimum ... Amount" chunks.
- **Category:** chunk boundary cut (with a retrieval miss component)
- **Root cause:** Fixed-size chunking split the heading from its value, and the value chunk
  shares few words with the question. Removing the fund name did not help, so the name
  is not the cause here.
- **Fix tried:** (fill in after the sentence-chunking results)

## Note on interpretation
I changed the chunking after seeing these misses, and the gold set has only 19 answerable
questions (one question is about 5 percentage points). So improvements measured on this
same set are probably optimistic, and small differences are not strong evidence.