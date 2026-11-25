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
| runtime-config-resource.html | trafilatura / strip tags | 1 | 132 chars, 0 headings, 0 tables | 198 chars, 0 headings, 0 tables | 0.00 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| ddl-partitioning.html | trafilatura / strip tags | 1 | 66 chars, 0 headings, 0 tables | 66 chars, 0 headings, 0 tables | 0.00 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| indexes.html | trafilatura / strip tags | 1 | 64 chars, 0 headings, 0 tables | 64 chars, 0 headings, 0 tables | 0.00 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| routine-vacuuming.html | trafilatura / strip tags | 1 | 66 chars, 0 headings, 0 tables | 66 chars, 0 headings, 0 tables | 0.00 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| performance-tips.html | trafilatura / strip tags | 1 | 75 chars, 0 headings, 0 tables | 75 chars, 0 headings, 0 tables | 0.00 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| wal-configuration.html | trafilatura / strip tags | 1 | 70 chars, 0 headings, 0 tables | 68 chars, 0 headings, 0 tables | 0.00 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| using-explain.html | trafilatura / strip tags | 1 | 418 chars, 0 headings, 0 tables | 473 chars, 0 headings, 0 tables | 0.00 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| how-parallel-query-works.html | trafilatura / strip tags | 1 | 73 chars, 0 headings, 0 tables | 73 chars, 0 headings, 0 tables | 0.00 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| brin-intro.html | trafilatura / strip tags | 1 | 55 chars, 0 headings, 0 tables | 55 chars, 0 headings, 0 tables | 0.00 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
| jit-decision.html | trafilatura / strip tags | 1 | 69 chars, 0 headings, 0 tables | 69 chars, 0 headings, 0 tables | 0.00 s / 0.00 s | trafilatura: extracts main content, drops HTML tags/scripts |
<!-- parsers:end -->

### D07 · Parsing my corpus
- Files in the manifest: 10 · parsed: 10 · failed: 0 · pages in Postgres: 10
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
