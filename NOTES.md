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
