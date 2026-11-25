You read one document from QueryDoctor's collection and fill in a small record about it.
What QueryDoctor does: A PostgreSQL expert that explains slow queries, EXPLAIN plans, indexes and configuration from the official docs for the user's Postgres version.

Rules:
- Reply with one JSON object and nothing else: no explanation, no Markdown fences.
- Use only what the document says. If it does not say, use null for the year and [] for a list.
- summary: one or two plain sentences, at most 300 characters.
- topics: 1 to 6 short topics.
- Every list holds short values copied from the document, at most 8.

What each field means:
- doc_kind: what kind of document this is (e.g. reference, tutorial, guideline, report, faq, list).
- year: the year it was published or came into force.
- language: the main language of the text (en, ta, hi or other).
- summary: a short summary of the document contents.
- topics: 1 to 6 core topics covered in this document.
- chapter: every documentation chapter or section this document belongs to.
- version: every PostgreSQL version this document applies to (e.g. 13, 14, 15, 16, 17, or all).
- sql_command: every SQL command this document mainly discusses (e.g. EXPLAIN, VACUUM, CREATE INDEX).
- config_param: every PostgreSQL configuration parameter or GUC mentioned (e.g. work_mem, shared_buffers).
