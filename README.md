# QueryDoctor

A PostgreSQL expert that explains slow queries, EXPLAIN plans, indexes and configuration from the official docs for the user's Postgres version.

**Status:** Day 1 foundation (FastAPI skeleton, quality gates). Live URL from Day 5.

## Who it's for

Backend developer at a Chennai SaaS company whose PostgreSQL queries became slow once a table crossed 50 million rows.

## The problem

The PostgreSQL official documentation is vast and changes significantly across versions. When queries slow down under large datasets, developers frequently paste EXPLAIN plans into public forums and receive advice that does not match their Postgres release. Key execution nodes, planner costs, and default memory parameters differ between versions 13 and 17. QueryDoctor solves this by providing version-specific explanations grounded directly in the official PostgreSQL manuals.

## Data sources

PostgreSQL documentation for versions 13-17 (SGML/HTML sources), release notes, and the PostgreSQL wiki performance pages.
- https://www.postgresql.org/docs/
- https://github.com/postgres/postgres (doc/src/sgml)
- Terms: PostgreSQL License (permissive).

## Hardest problem (my interview story)

Version-specific answers plus plan reading: behaviour and defaults change between versions, and the answer must combine the user's EXPLAIN ANALYZE text with the right doc pages. Each plan node must be explained with a version-correct citation.

## Signature feature

EXPLAIN explainer: paste EXPLAIN ANALYZE output and get each node explained with doc links and index suggestions.

## Target metric

Correct root cause for 80%+ of 30 slow-query cases with known fixes.

## Run it locally

```bash
uv sync
cp .env.example .env
# Windows: copy .env.example .env
uv run uvicorn querydoctor.api.main:create_app --factory --reload
```

Then open [http://localhost:8000/docs](http://localhost:8000/docs)

### Checks

```bash
uv run pytest
uv run ruff check .
```
