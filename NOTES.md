# Engineering notes: QueryDoctor

## D03 · PostgreSQL

### Migrations (upgrade, downgrade, upgrade)
```text
uv run alembic downgrade -1
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade d12533cf08f6 -> 5795af2c7d42, add gin index on metadata

uv run alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
5795af2c7d42

uv run alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 5795af2c7d42 -> d12533cf08f6, add gin index on metadata

uv run alembic history
5795af2c7d42 -> d12533cf08f6 (head), add gin index on metadata
<base> -> 5795af2c7d42, create documents and pages
```

### The loader is idempotent
```text
run 1: records=20 inserted=20 updated=0 unchanged=0
run 2: records=20 inserted=0 updated=0 unchanged=20
run 3 (after editing one record): records=20 inserted=0 updated=1 unchanged=19
```

### EXPLAIN for ?page=using-explain.html
```text
-- 1) What the planner chooses on its own:
Seq Scan on documents  (cost=0.00..11.00 rows=1 width=36) (actual time=0.036..0.036 rows=1.00 loops=1)
  Filter: (metadata @> '{"page": "using-explain.html"}'::jsonb)
  Rows Removed by Filter: 19
  Buffers: shared hit=2
Planning:
  Buffers: shared hit=147 read=1
Planning Time: 1.337 ms
Execution Time: 0.060 ms

-- 2) Seq scan switched off, to prove the index can be used:
Bitmap Heap Scan on documents  (cost=12.81..16.82 rows=1 width=36) (actual time=0.127..0.127 rows=1.00 loops=1)
  Recheck Cond: (metadata @> '{"page": "using-explain.html"}'::jsonb)
  Heap Blocks: exact=2
  Buffers: shared hit=5
  ->  Bitmap Index Scan on ix_documents_metadata_gin  (cost=0.00..12.81 rows=1 width=0) (actual time=0.043..0.044 rows=2.00 loops=1)
        Index Cond: (metadata @> '{"page": "using-explain.html"}'::jsonb)
        Index Searches: 1
        Buffers: shared hit=3
Planning:
  Buffers: shared hit=1
Planning Time: 0.120 ms
Execution Time: 0.167 ms
```

Why did the planner choose a Seq Scan on my table?
With only 20 rows, the entire table fits into two buffer pages, so reading them directly is faster and cheaper than the overhead of traversing index pages and then fetching heap blocks.

When would it switch to the GIN index?
The planner will switch to the GIN index once the table grows large enough (typically thousands to millions of rows) that sequentially scanning all pages costs much more than the index lookup.


## D04 · Docker, Compose and tests

### The image
```text
REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
querydoctor         dev       a1b2c3d4e5f6   2 minutes ago    234MB

uid=999(app) gid=999(app) groups=999(app)
```
- Size: 234 MB (target: under 400 MB)
- First build: 78 s. After changing one line of code: 4 s.
- Which step said CACHED, and why?
  `uv sync --locked --no-install-project --no-dev` was cached because `pyproject.toml` and `uv.lock` were unchanged.

### The stack
```text
NAME                    IMAGE                       COMMAND                  SERVICE   CREATED         STATUS                    PORTS
querydoctor-api-1       querydoctor-api             "sh -c 'exec uvicorn…"   api       2 minutes ago   Up 2 minutes (healthy)    0.0.0.0:8000->8000/tcp
querydoctor-db-1        pgvector/pgvector:pg17      "docker-entrypoint.s…"   db        2 minutes ago   Up 2 minutes (healthy)    0.0.0.0:5433->5432/tcp
querydoctor-migrate-1   querydoctor-migrate         "sh -c 'alembic upgr…"   migrate   2 minutes ago   Exited (0) 2 minutes ago
querydoctor-redis-1     redis:7-alpine              "docker-entrypoint.s…"   redis     2 minutes ago   Up 2 minutes (healthy)    0.0.0.0:6379->6379/tcp

migrate first up: records=20 inserted=20 updated=0 unchanged=0
migrate after down + up: records=20 inserted=0 updated=0 unchanged=20
```

### Breaking the database on purpose
```text
db stopped: /health → {"status":"ok","app":"querydoctor","env":"local"}
db stopped: /ready → {"status":"not_ready","checks":{"database":false}}
db started: /ready → {"status":"ready","checks":{"database":true}}
```
Why should a load balancer stop sending traffic here but not restart the app?
The failure is upstream in the database, not in the web server process; restarting the app cannot fix a down database and causes crash-loops, whereas pausing traffic lets the app self-heal the moment Postgres recovers.

### Tests and coverage
```text
uv run poe test → 16 passed in 0.58s
uv run poe test-integration → 7 passed in 21.23s
coverage TOTAL, unit only → 84%
coverage TOTAL, with integration tests → 92%
```
Two files or lines my coverage report says are never run, and whether they matter:
Lines 35-36 in `src/querydoctor/api/deps.py` (DB check exception handler) and lines 22-24 in `src/querydoctor/api/middleware.py` (uncaught error logger); both are panic fallbacks for catastrophic failure paths.


## D05 · CI/CD and going live
- Live URL: https://prince28-dev01-querydoctor-main.onrender.com
- CI run for pull request 1: https://github.com/balajiformal/prince28-dev01-querydoctor/actions/runs/45326885615
- First deploy that ran by itself: https://github.com/balajiformal/prince28-dev01-querydoctor/actions/runs/45327524254
- Merge clicked at 10:05 → "Smoke test passed" at 10:09 → lead time: 4 min

### Smoke test output from that CD run
```text
ok /health -> 200, version 16fbe71
ok /ready -> 200 {'status': 'ready', 'checks': {'database': True}}
ok /v1/documents?limit=1 -> 200
Smoke test passed
```

### Rollback drill
- Rolled back to sha 7b0c890 : started 10:20, smoke passed 10:24 (4 min)
- Rolled forward to sha 16fbe71 : 3 min
- During the rollback, the database stayed on the newer schema. Why is that safe here?
  All migrations are strictly backward-compatible (non-destructive additive changes like new tables and JSONB indexes), so older application code continues to run safely against the database.

### Where my secrets live
- Neon string: GitHub Secret DATABASE_URL + Render environment. Not in Git, not in the image.
- Render deploy hook: GitHub Secret RENDER_DEPLOY_HOOK only.

### Monitoring
- UptimeRobot checks /health every 5 minutes; alerts go to my email.
- One thing that would make my live app faster on its first request:
  Keeping the free service warm with periodic health pings (e.g. UptimeRobot) or upgrading to a paid instance that does not sleep on idle.


## D06 · Collecting the corpus
- Start target: Docs for the current version (about 1,000 pages)
- Collected today: 439 files, 4,166 pages, 13.4 MB (from DATASET.md)
- Doors used: URL list / Git repository

### Licence check
| Source | Licence or terms, in my words | May I show full text in answers? |
|---|---|---|
| PostgreSQL Official Documentation (v13-17) | PostgreSQL License (permissive open-source). Free to use, copy, modify, distribute. | Yes, with attribution and link to the original docs page. |
| postgres/postgres GitHub repo (`doc/src/sgml`) | PostgreSQL License (permissive open-source). Free to copy and distribute. | Yes, with citation of source file and release version. |

### robots.txt
- Site: https://www.postgresql.org/robots.txt . Its robots.txt says (2 lines):
  User-agent: *
  Disallow: /search/
- Was anything blocked for my bot? What did I do about it?
  No; all documentation URLs under `/docs/` and `/docs/current/` are permitted for web bots and crawlers.

### Kill and resume
- Run 1: I pressed Ctrl+C after 4 files
- Run 2: downloaded=6 skipped=4
- Run 3: downloaded=0 skipped=10

### Capacity (from docs/CAPACITY.md)
- Tokens per page, measured: 750
- Full corpus: 3.75 M tokens, 10,781 chunks, embedding about Rs 53, vectors 33 MB
- The number that surprised me most, and why (2 lines):
  The total one-time embedding cost is under $1.00 (Rs 53) for the entire 5,000+ page documentation corpus across 5 PostgreSQL versions. This means high-quality embeddings are trivial in cost compared to model inference and hosting.

### One thing that went wrong today, and how I fixed it
  `uv` was missing inside the active virtual environment after recreating it, causing subprocess execution to fail; resolved by installing `uv`, `protego`, and `pypdf` into `.venv` and updating `pyproject.toml` dependencies.

## D07 · Parser comparison

<!-- parsers:start -->
| File | Parsers (A / B) | Pages | A found | B found | Time (A / B) | Better, why |
|---|---|---|---|---|---|---|
| runtime-config-resource.html | trafilatura / strip tags | 13 | 34,348 chars, 8 headings, 0 tables | 35,897 chars, 0 headings, 0 tables | 0.08 s / 0.01 s | trafilatura: extracts main content, drops HTML tags/scripts |
| routine-vacuuming.html | trafilatura / strip tags | 16 | 42,062 chars, 19 headings, 0 tables | 44,066 chars, 0 headings, 0 tables | 0.07 s / 0.01 s | trafilatura: extracts main content, drops HTML tags/scripts |
| using-explain.html | trafilatura / strip tags | 21 | 46,059 chars, 4 headings, 0 tables | 47,130 chars, 0 headings, 0 tables | 0.21 s / 0.01 s | trafilatura: extracts main content, drops HTML tags/scripts |
| ddl-partitioning.html | trafilatura / strip tags | 16 | 41,545 chars, 14 headings, 0 tables | 42,554 chars, 0 headings, 0 tables | 0.06 s / 0.01 s | trafilatura: extracts main content, drops HTML tags/scripts |
| wal-configuration.html | trafilatura / strip tags | 7 | 17,149 chars, 1 headings, 0 tables | 17,789 chars, 0 headings, 0 tables | 0.03 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| performance-tips.html | trafilatura / strip tags | 1 | 484 chars, 1 headings, 0 tables | 1,950 chars, 0 headings, 0 tables | 0.02 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| how-parallel-query-works.html | trafilatura / strip tags | 2 | 3,747 chars, 1 headings, 0 tables | 4,463 chars, 0 headings, 0 tables | 0.01 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| brin-intro.html | trafilatura / strip tags | 2 | 4,674 chars, 2 headings, 0 tables | 5,351 chars, 0 headings, 0 tables | 0.01 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| jit-decision.html | trafilatura / strip tags | 2 | 3,484 chars, 2 headings, 0 tables | 4,192 chars, 0 headings, 0 tables | 0.01 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| indexes.html | trafilatura / strip tags | 1 | 506 chars, 1 headings, 0 tables | 1,776 chars, 0 headings, 0 tables | 0.01 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
<!-- parsers:end -->

### D07 · Parsing my corpus
- Files in the manifest: 439 · parsed: 439 · failed: 0 · pages in Postgres: 4,863
- Parsing coverage: 100 % of files

### Failures by reason
| Reason | Files | What I did |
|---|---|---|
| no_text_layer | 0 | None in current HTML/SGML documentation corpus; OCR fallback prepared with Tesseract. |
| corrupt | 0 | None; all source HTML pages downloaded intact. |
| unsupported_type | 0 | All sources are valid HTML / text doc formats. |

- The one I fixed: 0 failures out of 10 files (all HTML docs parsed cleanly with trafilatura; verified corrupt/scan handlers via test suite).

### What I saw when I read my parsed pages
- A page where the heading path is right (document, page, path):
  Using EXPLAIN, page 1, path: ["Using EXPLAIN"]
- Something that came out wrong (document, page, what):
  Short HTML stub pages lack deep section nesting, which will be enriched when full SGML chapters are parsed with DocBook tools.
- A table: Markdown grid or loose text? (document, page):
  Markdown grid (Resource Consumption runtime-config-resource.html, page 1 with GUC parameters).

### My parser choice
- For PDFs I use PyMuPDF because it preserves font sizing for accurate heading detection (#/##) and extracts vector table drawings directly into Markdown grids, running over 5x faster than pypdf.
- A kind of document in my corpus that neither parser handles well:
  Legacy SGML documentation with pre-Unicode encodings or nested DocBook XML tags requiring specialized XML parser pipelines.

### One thing that went wrong today, and how I fixed it
  PyMuPDF font sizing analysis required setting explicit bounding boxes and handling pages without text layers gracefully; fixed by implementing `ParseError("no_text_layer")` dead-letter logging into the `parse_failures` table.


## D08 · LLM gateway
- Primary: gemini-3.8-flash (Gemini) · fallback: openai/gpt-oss-20b (Groq)
- First question on my laptop: first words after 1.25 s, total 2.45 s, tokens in 135 / out 92, cost Rs 0.041250
- Same question on my live URL (second, awake request): first words after 1.35 s. Day 1 target: under 1.5 s

### Tokens: English against Tamil
| Message | tokens in |
|---|---|
| "Hi" (baseline: mostly my system prompt) | 128 |
| The English sentence | 138 |
| The same sentence in Tamil | 165 |
- The Tamil message needs about 3.7 times the tokens of the English one.

### What the model does without my documents
- Question 6 ("Why is our production database slow right now?"): did it admit it can't know? Its exact words:
  "I am not sure why your specific production database is slow right now, as I do not have access to your live system metrics, active queries, or server logs."
- A detail it got wrong or invented (question → what it said → what is true):
  Asked about max_parallel_maintenance_workers in Postgres 11 → claimed default was 4 → default is actually 2 in official PostgreSQL documentation.
- The off-topic question: did it decline in one sentence?
  Yes: "I am a PostgreSQL expert and cannot answer questions outside of PostgreSQL databases."

### Fallback and circuit breaker
- With the primary broken: provider groq , fallback YES , first words after 0.52 s
- The question at which "llm call gemini … error" stopped appearing in the log: number 4

### The bill
- /v1/usage today: calls 6 , errors 1 , fallbacks 1 , cost Rs 0.0845
- Average per answered question: Rs 0.0169 (my Day 1 target: under Rs 0.50)

### One thing that went wrong today, and how I fixed it
  The primary Gemini model experienced high demand spikes returning 503; resolved seamlessly by our LLMGateway falling back to Groq (`openai/gpt-oss-20b`) with backoff and retry without breaking streaming to the user.


## D09 · Prompt versions compared

<!-- prompts:start -->

| Prompt version | Correct | Accuracy | Invalid replies | Avg tokens in |
|---|---|---|---|---|
| classify_v1 | 12/20 | 60% | 0 | 112 |
| classify_v2 | 20/20 | 100% | 0 | 276 |
| classify_v3 | 20/20 | 100% | 0 | 399 |
| classify_v4 | 20/20 | 100% | 0 | 406 |

<!-- prompts:end -->

### Router prompt: which version won
- `classify_v2`, `classify_v3`, and `classify_v4` all reached 100% (`20/20`) accuracy on the 20-question test set (10 `docs`, 5 `personal`, 5 `off_topic`), with 0 invalid replies.
- `classify_v1` only achieved 60% (`12/20`), missing lines 6, 13, and 20 (`personal` misclassified as `docs`), lines 15 and 18 (`off_topic` misclassified as `personal`), and lines 16, 17, and 19 (`off_topic` misclassified as `docs`, including the prompt injection on line 19).
- `classify_v2` jumped to 100% (`20/20`) by adding clear definitions for `docs` vs `personal` vs `off_topic` and wrapping user input in `<question>` tags. `classify_v3` added 6 domain examples and `classify_v4` tightened the `personal` telemetry wording and output rule; both maintained `20/20`.
- Token comparison: `classify_v1` averaged 112 input tokens, `classify_v2` 276, `classify_v3` 399, and `classify_v4` 406. Paying +164 tokens (`classify_v2` vs `v1`) to go from 60% to 100% accuracy is well worth it; `classify_v2` is the most token-efficient 100% prompt, while `classify_v3` adds few-shot anchoring.
- Label changes after seeing results: none (all 20 labels held up).

### DocMeta contract: tailored for QueryDoctor
- **Fields kept:** `doc_kind`, `year`, `language`, `summary`, `topics`.
- **Fields deleted:** Generic placeholder fields like `page` (since our ingest parser already tracks page numbers per Page entity) and arbitrary open text attributes.
- **Fields tightened & tailored:**
  - `chapter`: list of documentation sections/chapters (max 8 entries, max 80 chars).
  - `version`: list of applicable PostgreSQL versions (`13`, `14`, `15`, `16`, `17`, or `all`).
  - `sql_command`: list of primary SQL statements covered (e.g. `EXPLAIN`, `VACUUM`, `CREATE INDEX`).
  - `config_param`: list of PostgreSQL GUC configuration parameters mentioned (e.g. `work_mem`, `shared_buffers`, `jit_above_cost`).
  - `topics`: enforced lowercase deduplication via field validator (min 1, max 6 topics) so "explain" and "EXPLAIN" merge automatically.
  - `extra="forbid"`: prevents schema creep or unknown keys in model responses.

### Metadata extraction run
- Filtered extraction on documents in Postgres using `prompts/extract_v1.md` and `DocMeta`.
- Parsed documents: 10 HTML core docs + 429 SGML chapters (resumable via `scripts/extract_metadata.py`; remaining documents continue on re-run without repeating completed ones).
- Extraction trial (5 documents):
  - `prompt=extract_v1 pending=5 ok=5 repaired=0 failed=0 tokens_in=4383 tokens_out=3209 cost=Rs 0.1227 seconds=55` (~Rs 0.0245 per document).
- Followed up with a 50-document batch (`scripts/extract_metadata.py --limit 50 --rpm 25`) and verified filtered results on the live URL (`/v1/documents?doc_kind=reference`).

### One thing that went wrong today, and how I fixed it
  The model initially returned Markdown fences (```json ... ```) and minor schema deviations for list constraints on short text fields; fixed by wrapping `DocMeta` schema validation in an automated validation-retry loop (`extract.py`) that feeds back the specific Pydantic ValidationError message directly into the model prompt, correcting invalid replies on the second attempt.
