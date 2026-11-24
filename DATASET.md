# Dataset: QueryDoctor

A PostgreSQL expert that explains slow queries, EXPLAIN plans, indexes and configuration from the official docs for the user's Postgres version.

- **Start target:** Docs for the current version (about 1,000 pages)
- **Full target:** Docs for 5 versions + all release notes (5,000+ pages)
- **Collected by:** `scripts/fetch.py` as `examate-student-bot` (https://github.com/balajiformal/prince28-dev01-querydoctor): robots.txt respected, at most 4 requests at once, 0.5 s between requests to one site.

## Where the documents come from

- https://www.postgresql.org/docs/
- https://github.com/postgres/postgres (doc/src/sgml)

## Terms I follow

PostgreSQL License (permissive).
- Every answer links to the original document.
- No personal data is collected.

<!-- generated:start -->
## Sources (generated 2026-11-24 06:10 UTC by scripts/dataset_report.py)

| Source | Licence / terms | Files | MB | Pages* | How | Fetched | Example URL |
|---|---|---|---|---|---|---|---|
| postgres-docs | PostgreSQL License (permissive). | 10 | 0.5 | 184 | http | 2026-11-24 | https://www.postgresql.org/docs/current/using-explain.html |

**Total:** 10 files, 0.5 MB, 184 pages. Not downloaded: 0 blocked by robots.txt, 0 failed.

*Pages = PDF pages, plus one page per 3,000 characters of text or HTML.

## Files (first 10 of 10)

The complete list, with a sha256 fingerprint of every file, is `data/manifest.jsonl`.

| # | Title / file | Source | Pages | Fetched | URL |
|---|---|---|---|---|---|
| 1 | BRIN Indexes | postgres-docs | 12 | 2026-11-24 | https://www.postgresql.org/docs/current/brin-intro.html |
| 2 | Table Partitioning | postgres-docs | 25 | 2026-11-24 | https://www.postgresql.org/docs/current/ddl-partitioning.html |
| 3 | How Parallel Query Works | postgres-docs | 14 | 2026-11-24 | https://www.postgresql.org/docs/current/how-parallel-query-works.html |
| 4 | Indexes Overview | postgres-docs | 22 | 2026-11-24 | https://www.postgresql.org/docs/current/indexes.html |
| 5 | Just-in-Time Compilation | postgres-docs | 10 | 2026-11-24 | https://www.postgresql.org/docs/current/jit-decision.html |
| 6 | Performance Tips | postgres-docs | 20 | 2026-11-24 | https://www.postgresql.org/docs/current/performance-tips.html |
| 7 | Routine Vacuuming | postgres-docs | 20 | 2026-11-24 | https://www.postgresql.org/docs/current/routine-vacuuming.html |
| 8 | Resource Consumption | postgres-docs | 27 | 2026-11-24 | https://www.postgresql.org/docs/current/runtime-config-resource.html |
| 9 | Using EXPLAIN | postgres-docs | 16 | 2026-11-24 | https://www.postgresql.org/docs/current/using-explain.html |
| 10 | WAL Configuration | postgres-docs | 18 | 2026-11-24 | https://www.postgresql.org/docs/current/wal-configuration.html |
<!-- generated:end -->

## Known gaps

- Release notes and legacy version-specific documentation (v13-v16) will be ingested during Week 2 expansion.
- SGML build tools and HTML post-processing will be added in Day 7 document parsing.
