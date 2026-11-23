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
