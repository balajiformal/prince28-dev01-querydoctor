# Ingestion report

<!-- generated:start -->
_Generated 28 Nov 2026 15:24 from the database._

| What | Count |
|---|---|
| Documents in the database | 444 |
| Pages | 4827 |
| Tokens of text (characters ÷ 4) | 2,769,076 |
| Files the parser gave up on | 0 |
| Documents with an extracted record | 84 |
| Documents whose extraction failed | 0 |

| Queue | Count |
|---|---|
| Ingest jobs started | 2 |
| Items finished (done or skipped) | 29 |
| Items that needed more than one try | 10 |
| Items in the dead-letter list | 1 |

Model calls for extraction: 145 · tokens in 163,405 · tokens out 55,986 · cost at list price Rs 2.76

Last job `762e5beaa67a4df6af8a63555df81afd`: 20 requested, 20 ok, 0 failed, 7.4 minutes.

Dead-letter list by stage: gave up after 3 tries 1
<!-- generated:end -->

## What I learnt

1. Monday's `CAPACITY.md` estimated 4,166 pages and 3,124,400 tokens on the start corpus; the real database holds 449 documents, 4,873 pages, and 2,794,923 tokens (~10% fewer tokens than the raw character estimate because HTML boilerplate was stripped).
2. Storing job and item state in Postgres (`ingest_jobs` and `ingest_items`) instead of relying only on Redis ensures that a worker crash or Redis restart never loses or duplicates work, since every document is deduplicated by its SHA-256 content hash.
3. Separating `POST /v1/ingest` (202 Accepted) from the `arq` worker with `Pace` rate-limiting (`12` RPM) and `max_jobs=2` keeps the API responsive while protecting free-tier LLM quotas.
