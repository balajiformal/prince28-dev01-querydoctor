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
## Sources (generated 2026-11-25 05:50 UTC by scripts/dataset_report.py)

| Source | Licence / terms | Files | MB | Pages* | How | Fetched | Example URL |
|---|---|---|---|---|---|---|---|
| postgres-docs | PostgreSQL License (permissive). | 10 | 0.6 | 0 | http | 2026-11-24 | https://www.postgresql.org/docs/current/using-explain.html |
| postgres-sgml | PostgreSQL License (permissive). | 429 | 12.8 | 4,165 | git @ c7f5cf46c9 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/acronyms.sgml |

**Total:** 439 files, 13.4 MB, 4,166 pages. Not downloaded: 0 blocked by robots.txt, 0 failed.

*Pages = PDF pages, plus one page per 3,000 characters of text or HTML.

## Files (first 200 of 439)

The complete list, with a sha256 fingerprint of every file, is `data/manifest.jsonl`.

| # | Title / file | Source | Pages | Fetched | URL |
|---|---|---|---|---|---|
| 1 | BRIN Indexes | postgres-docs |  | 2026-11-24 | https://www.postgresql.org/docs/current/brin-intro.html |
| 2 | Table Partitioning | postgres-docs |  | 2026-11-24 | https://www.postgresql.org/docs/current/ddl-partitioning.html |
| 3 | How Parallel Query Works | postgres-docs |  | 2026-11-24 | https://www.postgresql.org/docs/current/how-parallel-query-works.html |
| 4 | Indexes Overview | postgres-docs |  | 2026-11-24 | https://www.postgresql.org/docs/current/indexes.html |
| 5 | Just-in-Time Compilation | postgres-docs |  | 2026-11-24 | https://www.postgresql.org/docs/current/jit-decision.html |
| 6 | Performance Tips | postgres-docs |  | 2026-11-24 | https://www.postgresql.org/docs/current/performance-tips.html |
| 7 | Routine Vacuuming | postgres-docs |  | 2026-11-24 | https://www.postgresql.org/docs/current/routine-vacuuming.html |
| 8 | Resource Consumption | postgres-docs |  | 2026-11-24 | https://www.postgresql.org/docs/current/runtime-config-resource.html |
| 9 | Using EXPLAIN | postgres-docs |  | 2026-11-24 | https://www.postgresql.org/docs/current/using-explain.html |
| 10 | WAL Configuration | postgres-docs |  | 2026-11-24 | https://www.postgresql.org/docs/current/wal-configuration.html |
| 11 | doc/src/sgml/acronyms.sgml | postgres-sgml | 7 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/acronyms.sgml |
| 12 | doc/src/sgml/advanced.sgml | postgres-sgml | 9 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/advanced.sgml |
| 13 | doc/src/sgml/amcheck.sgml | postgres-sgml | 8 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/amcheck.sgml |
| 14 | doc/src/sgml/appendix-obsolete-auth-radius.sgml | postgres-sgml |  | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/appendix-obsolete-auth-radius.sgml |
| 15 | doc/src/sgml/appendix-obsolete-default-roles.sgml | postgres-sgml |  | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/appendix-obsolete-default-roles.sgml |
| 16 | doc/src/sgml/appendix-obsolete-libpq-fastpath.sgml | postgres-sgml |  | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/appendix-obsolete-libpq-fastpath.sgml |
| 17 | doc/src/sgml/appendix-obsolete-pgreceivexlog.sgml | postgres-sgml |  | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/appendix-obsolete-pgreceivexlog.sgml |
| 18 | doc/src/sgml/appendix-obsolete-pgresetxlog.sgml | postgres-sgml |  | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/appendix-obsolete-pgresetxlog.sgml |
| 19 | doc/src/sgml/appendix-obsolete-pgxlogdump.sgml | postgres-sgml |  | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/appendix-obsolete-pgxlogdump.sgml |
| 20 | doc/src/sgml/appendix-obsolete-recovery-config.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/appendix-obsolete-recovery-config.sgml |
| 21 | doc/src/sgml/appendix-obsolete-refint.sgml | postgres-sgml |  | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/appendix-obsolete-refint.sgml |
| 22 | doc/src/sgml/appendix-obsolete.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/appendix-obsolete.sgml |
| 23 | doc/src/sgml/arch-dev.sgml | postgres-sgml | 8 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/arch-dev.sgml |
| 24 | doc/src/sgml/archive-modules.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/archive-modules.sgml |
| 25 | doc/src/sgml/array.sgml | postgres-sgml | 9 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/array.sgml |
| 26 | doc/src/sgml/auth-delay.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/auth-delay.sgml |
| 27 | doc/src/sgml/auto-explain.sgml | postgres-sgml | 5 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/auto-explain.sgml |
| 28 | doc/src/sgml/backup-manifest.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/backup-manifest.sgml |
| 29 | doc/src/sgml/backup.sgml | postgres-sgml | 26 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/backup.sgml |
| 30 | doc/src/sgml/basebackup-to-shell.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/basebackup-to-shell.sgml |
| 31 | doc/src/sgml/basic-archive.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/basic-archive.sgml |
| 32 | doc/src/sgml/bgworker.sgml | postgres-sgml | 6 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/bgworker.sgml |
| 33 | doc/src/sgml/biblio.sgml | postgres-sgml | 6 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/biblio.sgml |
| 34 | doc/src/sgml/bki.sgml | postgres-sgml | 15 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/bki.sgml |
| 35 | doc/src/sgml/bloom.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/bloom.sgml |
| 36 | doc/src/sgml/brin.sgml | postgres-sgml | 18 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/brin.sgml |
| 37 | doc/src/sgml/btree-gin.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/btree-gin.sgml |
| 38 | doc/src/sgml/btree-gist.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/btree-gist.sgml |
| 39 | doc/src/sgml/btree.sgml | postgres-sgml | 14 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/btree.sgml |
| 40 | doc/src/sgml/catalogs.sgml | postgres-sgml | 115 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/catalogs.sgml |
| 41 | doc/src/sgml/charset.sgml | postgres-sgml | 41 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/charset.sgml |
| 42 | doc/src/sgml/citext.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/citext.sgml |
| 43 | doc/src/sgml/client-auth.sgml | postgres-sgml | 36 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/client-auth.sgml |
| 44 | doc/src/sgml/color.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/color.sgml |
| 45 | doc/src/sgml/config.sgml | postgres-sgml | 204 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/config.sgml |
| 46 | doc/src/sgml/contrib-spi.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/contrib-spi.sgml |
| 47 | doc/src/sgml/contrib.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/contrib.sgml |
| 48 | doc/src/sgml/cube.sgml | postgres-sgml | 7 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/cube.sgml |
| 49 | doc/src/sgml/custom-rmgr.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/custom-rmgr.sgml |
| 50 | doc/src/sgml/custom-scan.sgml | postgres-sgml | 6 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/custom-scan.sgml |
| 51 | doc/src/sgml/datatype.sgml | postgres-sgml | 66 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/datatype.sgml |
| 52 | doc/src/sgml/datetime.sgml | postgres-sgml | 12 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/datetime.sgml |
| 53 | doc/src/sgml/dblink.sgml | postgres-sgml | 20 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/dblink.sgml |
| 54 | doc/src/sgml/ddl.sgml | postgres-sgml | 75 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ddl.sgml |
| 55 | doc/src/sgml/dfunc.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/dfunc.sgml |
| 56 | doc/src/sgml/dict-int.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/dict-int.sgml |
| 57 | doc/src/sgml/dict-xsyn.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/dict-xsyn.sgml |
| 58 | doc/src/sgml/dml.sgml | postgres-sgml | 5 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/dml.sgml |
| 59 | doc/src/sgml/docguide.sgml | postgres-sgml | 7 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/docguide.sgml |
| 60 | doc/src/sgml/earthdistance.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/earthdistance.sgml |
| 61 | doc/src/sgml/ecpg.sgml | postgres-sgml | 111 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ecpg.sgml |
| 62 | doc/src/sgml/errcodes.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/errcodes.sgml |
| 63 | doc/src/sgml/event-trigger.sgml | postgres-sgml | 6 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/event-trigger.sgml |
| 64 | doc/src/sgml/extend.sgml | postgres-sgml | 28 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/extend.sgml |
| 65 | doc/src/sgml/external-projects.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/external-projects.sgml |
| 66 | doc/src/sgml/fdwhandler.sgml | postgres-sgml | 34 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/fdwhandler.sgml |
| 67 | doc/src/sgml/features.sgml | postgres-sgml | 7 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/features.sgml |
| 68 | doc/src/sgml/file-fdw.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/file-fdw.sgml |
| 69 | doc/src/sgml/filelist.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/filelist.sgml |
| 70 | doc/src/sgml/func/allfiles.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/allfiles.sgml |
| 71 | doc/src/sgml/func/func-admin.sgml | postgres-sgml | 46 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-admin.sgml |
| 72 | doc/src/sgml/func/func-aggregate.sgml | postgres-sgml | 18 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-aggregate.sgml |
| 73 | doc/src/sgml/func/func-array.sgml | postgres-sgml | 8 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-array.sgml |
| 74 | doc/src/sgml/func/func-binarystring.sgml | postgres-sgml | 11 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-binarystring.sgml |
| 75 | doc/src/sgml/func/func-bitstring.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-bitstring.sgml |
| 76 | doc/src/sgml/func/func-comparison.sgml | postgres-sgml | 8 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-comparison.sgml |
| 77 | doc/src/sgml/func/func-comparisons.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-comparisons.sgml |
| 78 | doc/src/sgml/func/func-conditional.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-conditional.sgml |
| 79 | doc/src/sgml/func/func-datetime.sgml | postgres-sgml | 28 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-datetime.sgml |
| 80 | doc/src/sgml/func/func-enum.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-enum.sgml |
| 81 | doc/src/sgml/func/func-event-triggers.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-event-triggers.sgml |
| 82 | doc/src/sgml/func/func-formatting.sgml | postgres-sgml | 15 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-formatting.sgml |
| 83 | doc/src/sgml/func/func-geometry.sgml | postgres-sgml | 15 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-geometry.sgml |
| 84 | doc/src/sgml/func/func-info.sgml | postgres-sgml | 50 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-info.sgml |
| 85 | doc/src/sgml/func/func-json.sgml | postgres-sgml | 57 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-json.sgml |
| 86 | doc/src/sgml/func/func-logical.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-logical.sgml |
| 87 | doc/src/sgml/func/func-matching.sgml | postgres-sgml | 34 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-matching.sgml |
| 88 | doc/src/sgml/func/func-math.sgml | postgres-sgml | 17 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-math.sgml |
| 89 | doc/src/sgml/func/func-merge-support.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-merge-support.sgml |
| 90 | doc/src/sgml/func/func-net.sgml | postgres-sgml | 6 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-net.sgml |
| 91 | doc/src/sgml/func/func-range.sgml | postgres-sgml | 12 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-range.sgml |
| 92 | doc/src/sgml/func/func-sequence.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-sequence.sgml |
| 93 | doc/src/sgml/func/func-srf.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-srf.sgml |
| 94 | doc/src/sgml/func/func-statistics.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-statistics.sgml |
| 95 | doc/src/sgml/func/func-string.sgml | postgres-sgml | 24 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-string.sgml |
| 96 | doc/src/sgml/func/func-subquery.sgml | postgres-sgml | 5 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-subquery.sgml |
| 97 | doc/src/sgml/func/func-textsearch.sgml | postgres-sgml | 14 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-textsearch.sgml |
| 98 | doc/src/sgml/func/func-tid.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-tid.sgml |
| 99 | doc/src/sgml/func/func-trigger.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-trigger.sgml |
| 100 | doc/src/sgml/func/func-uuid.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-uuid.sgml |
| 101 | doc/src/sgml/func/func-window.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-window.sgml |
| 102 | doc/src/sgml/func/func-xml.sgml | postgres-sgml | 16 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func-xml.sgml |
| 103 | doc/src/sgml/func/func.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/func/func.sgml |
| 104 | doc/src/sgml/fuzzystrmatch.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/fuzzystrmatch.sgml |
| 105 | doc/src/sgml/generic-wal.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/generic-wal.sgml |
| 106 | doc/src/sgml/geqo.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/geqo.sgml |
| 107 | doc/src/sgml/gin.sgml | postgres-sgml | 10 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/gin.sgml |
| 108 | doc/src/sgml/gist.sgml | postgres-sgml | 18 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/gist.sgml |
| 109 | doc/src/sgml/glossary.sgml | postgres-sgml | 29 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/glossary.sgml |
| 110 | doc/src/sgml/hash.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/hash.sgml |
| 111 | doc/src/sgml/high-availability.sgml | postgres-sgml | 36 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/high-availability.sgml |
| 112 | doc/src/sgml/history.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/history.sgml |
| 113 | doc/src/sgml/hstore.sgml | postgres-sgml | 11 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/hstore.sgml |
| 114 | doc/src/sgml/indexam.sgml | postgres-sgml | 24 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/indexam.sgml |
| 115 | doc/src/sgml/indextypes.sgml | postgres-sgml |  | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/indextypes.sgml |
| 116 | doc/src/sgml/indices.sgml | postgres-sgml | 24 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/indices.sgml |
| 117 | doc/src/sgml/info.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/info.sgml |
| 118 | doc/src/sgml/information_schema.sgml | postgres-sgml | 95 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/information_schema.sgml |
| 119 | doc/src/sgml/install-binaries.sgml | postgres-sgml |  | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/install-binaries.sgml |
| 120 | doc/src/sgml/installation.sgml | postgres-sgml | 52 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/installation.sgml |
| 121 | doc/src/sgml/intagg.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/intagg.sgml |
| 122 | doc/src/sgml/intarray.sgml | postgres-sgml | 6 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/intarray.sgml |
| 123 | doc/src/sgml/intro.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/intro.sgml |
| 124 | doc/src/sgml/isn.sgml | postgres-sgml | 5 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/isn.sgml |
| 125 | doc/src/sgml/jit.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/jit.sgml |
| 126 | doc/src/sgml/json.sgml | postgres-sgml | 14 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/json.sgml |
| 127 | doc/src/sgml/keywords.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/keywords.sgml |
| 128 | doc/src/sgml/legal.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/legal.sgml |
| 129 | doc/src/sgml/libpq.sgml | postgres-sgml | 150 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/libpq.sgml |
| 130 | doc/src/sgml/limits.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/limits.sgml |
| 131 | doc/src/sgml/lo.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/lo.sgml |
| 132 | doc/src/sgml/lobj.sgml | postgres-sgml | 12 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/lobj.sgml |
| 133 | doc/src/sgml/logical-replication.sgml | postgres-sgml | 51 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/logical-replication.sgml |
| 134 | doc/src/sgml/logicaldecoding.sgml | postgres-sgml | 26 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/logicaldecoding.sgml |
| 135 | doc/src/sgml/ltree.sgml | postgres-sgml | 10 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ltree.sgml |
| 136 | doc/src/sgml/maintenance.sgml | postgres-sgml | 23 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/maintenance.sgml |
| 137 | doc/src/sgml/manage-ag.sgml | postgres-sgml | 8 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/manage-ag.sgml |
| 138 | doc/src/sgml/monitoring.sgml | postgres-sgml | 109 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/monitoring.sgml |
| 139 | doc/src/sgml/mvcc.sgml | postgres-sgml | 28 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/mvcc.sgml |
| 140 | doc/src/sgml/nls.sgml | postgres-sgml | 7 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/nls.sgml |
| 141 | doc/src/sgml/notation.sgml | postgres-sgml |  | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/notation.sgml |
| 142 | doc/src/sgml/oauth-validators.sgml | postgres-sgml | 10 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/oauth-validators.sgml |
| 143 | doc/src/sgml/oid2name.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/oid2name.sgml |
| 144 | doc/src/sgml/pageinspect.sgml | postgres-sgml | 11 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pageinspect.sgml |
| 145 | doc/src/sgml/parallel.sgml | postgres-sgml | 9 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/parallel.sgml |
| 146 | doc/src/sgml/passwordcheck.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/passwordcheck.sgml |
| 147 | doc/src/sgml/perform.sgml | postgres-sgml | 35 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/perform.sgml |
| 148 | doc/src/sgml/pgbuffercache.sgml | postgres-sgml | 9 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgbuffercache.sgml |
| 149 | doc/src/sgml/pgcrypto.sgml | postgres-sgml | 14 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgcrypto.sgml |
| 150 | doc/src/sgml/pgfreespacemap.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgfreespacemap.sgml |
| 151 | doc/src/sgml/pglogicalinspect.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pglogicalinspect.sgml |
| 152 | doc/src/sgml/pgoverexplain.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgoverexplain.sgml |
| 153 | doc/src/sgml/pgplanadvice.sgml | postgres-sgml | 12 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgplanadvice.sgml |
| 154 | doc/src/sgml/pgprewarm.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgprewarm.sgml |
| 155 | doc/src/sgml/pgrowlocks.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgrowlocks.sgml |
| 156 | doc/src/sgml/pgstashadvice.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgstashadvice.sgml |
| 157 | doc/src/sgml/pgstatstatements.sgml | postgres-sgml | 15 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgstatstatements.sgml |
| 158 | doc/src/sgml/pgstattuple.sgml | postgres-sgml | 6 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgstattuple.sgml |
| 159 | doc/src/sgml/pgsurgery.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgsurgery.sgml |
| 160 | doc/src/sgml/pgtrgm.sgml | postgres-sgml | 8 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgtrgm.sgml |
| 161 | doc/src/sgml/pgvisibility.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgvisibility.sgml |
| 162 | doc/src/sgml/pgwalinspect.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pgwalinspect.sgml |
| 163 | doc/src/sgml/planstats.sgml | postgres-sgml | 11 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/planstats.sgml |
| 164 | doc/src/sgml/plhandler.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/plhandler.sgml |
| 165 | doc/src/sgml/plperl.sgml | postgres-sgml | 19 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/plperl.sgml |
| 166 | doc/src/sgml/plpgsql.sgml | postgres-sgml | 78 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/plpgsql.sgml |
| 167 | doc/src/sgml/plpython.sgml | postgres-sgml | 17 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/plpython.sgml |
| 168 | doc/src/sgml/pltcl.sgml | postgres-sgml | 15 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/pltcl.sgml |
| 169 | doc/src/sgml/postgres-fdw.sgml | postgres-sgml | 21 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/postgres-fdw.sgml |
| 170 | doc/src/sgml/postgres.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/postgres.sgml |
| 171 | doc/src/sgml/problems.sgml | postgres-sgml | 5 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/problems.sgml |
| 172 | doc/src/sgml/protocol.sgml | postgres-sgml | 88 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/protocol.sgml |
| 173 | doc/src/sgml/queries.sgml | postgres-sgml | 35 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/queries.sgml |
| 174 | doc/src/sgml/query.sgml | postgres-sgml | 11 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/query.sgml |
| 175 | doc/src/sgml/rangetypes.sgml | postgres-sgml | 7 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/rangetypes.sgml |
| 176 | doc/src/sgml/ref/abort.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/abort.sgml |
| 177 | doc/src/sgml/ref/allfiles.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/allfiles.sgml |
| 178 | doc/src/sgml/ref/alter_aggregate.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_aggregate.sgml |
| 179 | doc/src/sgml/ref/alter_collation.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_collation.sgml |
| 180 | doc/src/sgml/ref/alter_conversion.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_conversion.sgml |
| 181 | doc/src/sgml/ref/alter_database.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_database.sgml |
| 182 | doc/src/sgml/ref/alter_default_privileges.sgml | postgres-sgml | 3 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_default_privileges.sgml |
| 183 | doc/src/sgml/ref/alter_domain.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_domain.sgml |
| 184 | doc/src/sgml/ref/alter_event_trigger.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_event_trigger.sgml |
| 185 | doc/src/sgml/ref/alter_extension.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_extension.sgml |
| 186 | doc/src/sgml/ref/alter_foreign_data_wrapper.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_foreign_data_wrapper.sgml |
| 187 | doc/src/sgml/ref/alter_foreign_table.sgml | postgres-sgml | 7 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_foreign_table.sgml |
| 188 | doc/src/sgml/ref/alter_function.sgml | postgres-sgml | 5 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_function.sgml |
| 189 | doc/src/sgml/ref/alter_group.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_group.sgml |
| 190 | doc/src/sgml/ref/alter_index.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_index.sgml |
| 191 | doc/src/sgml/ref/alter_language.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_language.sgml |
| 192 | doc/src/sgml/ref/alter_large_object.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_large_object.sgml |
| 193 | doc/src/sgml/ref/alter_materialized_view.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_materialized_view.sgml |
| 194 | doc/src/sgml/ref/alter_opclass.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_opclass.sgml |
| 195 | doc/src/sgml/ref/alter_operator.sgml | postgres-sgml | 2 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_operator.sgml |
| 196 | doc/src/sgml/ref/alter_opfamily.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_opfamily.sgml |
| 197 | doc/src/sgml/ref/alter_policy.sgml | postgres-sgml | 1 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_policy.sgml |
| 198 | doc/src/sgml/ref/alter_procedure.sgml | postgres-sgml | 4 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_procedure.sgml |
| 199 | doc/src/sgml/ref/alter_publication.sgml | postgres-sgml | 5 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_publication.sgml |
| 200 | doc/src/sgml/ref/alter_role.sgml | postgres-sgml | 5 | 2026-11-25 | https://github.com/postgres/postgres/blob/HEAD/doc/src/sgml/ref/alter_role.sgml |
<!-- generated:end -->

## Known gaps

- Release notes and legacy version-specific documentation (v13-v16) will be ingested during Week 2 expansion.
- SGML build tools and HTML post-processing will be added in Day 7 document parsing.
