# Capacity plan: QueryDoctor

Full corpus target: Docs for 5 versions + all release notes (5,000+ pages)

<!-- generated:start -->
## Measured on my start corpus (2026-11-24 06:10 UTC)

| What | Value |
|---|---|
| Files | 10 |
| Size on disk | 0.5 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 184 |
| Characters of text | 552,000 |
| Estimated tokens (characters / 4) | 138,000 |
| Tokens per page | 750 |
| PDFs with almost no text (scanned? OCR is Day 7) | 0 |
| Files not measured (zip, xlsx, unreadable) | 0 |

## Estimate for the full corpus (target: 5,000 pages)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 27.2 |
| Tokens | measured tokens x scale | 3.75 M |
| Raw files | measured MB x scale | 14 MB |
| Chunks | tokens / 400 x 1.15 overlap | 10,781 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.56 = Rs 53 |
| Vector storage | chunks x 768 numbers x 4 bytes | 33 MB |
| Text in Postgres | characters x scale x 1.2 | 18 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->

## What I conclude

1. Is embedding cost a problem for this product?
   No; embedding 5,000 pages (~4-5M tokens) costs under $1.00 (approx. Rs 70-95), which is negligible.
2. Do the vectors and text fit in my free Postgres?
   Yes; the combined vector and text storage requires under 50 MB, well within Neon's 500 MB free tier storage limit.
3. Which number above am I least sure about, and how will I measure it better?
   Characters per token (currently assumed at 4); on Day 8 we will tokenize with tiktoken/cl100k_base to get exact token counts.
4. What changes if the corpus grows 10 times?
   Storage will grow to ~500 MB, approaching free-tier limits, requiring Neon compute/storage scale-up or vector indexing via HNSW with half-precision fp16.
