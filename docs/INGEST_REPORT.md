# Ingestion report

<!-- generated:start -->
_Generated 27 Nov 2026 15:02 from the database._

| What | Count |
|---|---|
| Documents in the database | 449 |
| Pages | 4873 |
| Tokens of text (characters ÷ 4) | 2,794,923 |
| Files the parser gave up on | 0 |
| Documents with an extracted record | 55 |
| Documents whose extraction failed | 0 |

| Queue | Count |
|---|---|
| Ingest jobs started | 0 |
| Items finished (done or skipped) | 0 |
| Items that needed more than one try | 0 |
| Items in the dead-letter list | 0 |

Model calls for extraction: 82 · tokens in 93,649 · tokens out 36,481 · cost at list price Rs 1.71
<!-- generated:end -->

## What I learnt

1. Monday's `CAPACITY.md` estimated 4,166 pages and 3,124,400 tokens on the start corpus; the real database holds 449 documents, 4,873 pages, and 2,794,923 tokens (~10% fewer tokens than the raw character estimate because HTML boilerplate was stripped).
2. Storing job and item state in Postgres (`ingest_jobs` and `ingest_items`) instead of relying only on Redis ensures that a worker crash or Redis restart never loses or duplicates work, since every document is deduplicated by its SHA-256 content hash.
3. Separating `POST /v1/ingest` (202 Accepted) from the `arq` worker with `Pace` rate-limiting (`12` RPM) and `max_jobs=2` keeps the API responsive while protecting free-tier LLM quotas.
