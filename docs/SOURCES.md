# Data Sources: QueryDoctor

## Record Schema
Each corpus record contains the following fields:
- `id`: Unique identifier string (e.g. `pg15-using-explain`)
- `page`: Filename or URL slug of the official documentation page (e.g. `using-explain.html`)
- `chapter`: Documentation chapter title or category (e.g. `Performance Tips`)
- `version`: Target PostgreSQL major version (`13`, `14`, `15`, `16`, `17`)
- `topic`: Core subject matter (e.g. `EXPLAIN Planner Cost`, `Memory Configuration`, `Indexes`)
- `sql_command`: Related SQL statement or syntax (e.g. `EXPLAIN (ANALYZE, BUFFERS)`, `VACUUM FULL`)
- `config_param`: Configuration setting name (e.g. `work_mem`, `random_page_cost`, `shared_buffers`)

## Primary Sources
| Source Name | Location / URL | Format | Terms of Use |
|---|---|---|---|
| PostgreSQL Official Documentation (v13-17) | https://www.postgresql.org/docs/ | HTML | PostgreSQL License (permissive open-source) |
| PostgreSQL Source Repository (`doc/src/sgml`) | https://github.com/postgres/postgres | SGML / DocBook | PostgreSQL License (permissive open-source) |
| PostgreSQL Release Notes (v13-17) | https://www.postgresql.org/docs/release/ | HTML | PostgreSQL License (permissive open-source) |
| PostgreSQL Community Performance Wiki | https://wiki.postgresql.org/wiki/Performance_Optimization | Wiki text / HTML | PostgreSQL License / Creative Commons |
