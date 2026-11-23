# Requirements

## Functional Requirements

1. Support diagnostic guidance, plan explanation, and configuration parameter documentation across 5 major PostgreSQL versions (13, 14, 15, 16, and 17).
2. Expose a paginated `GET /v1/documents` endpoint supporting search filtering via query parameter `q` (max 200 characters) and pagination controls (`limit` between 1 and 100, default 20; `offset` >= 0).
3. Expose `GET /v1/documents/{doc_id}` returning a single document record by unique string ID, returning HTTP 404 with RFC 9457 problem details if not found.
4. Correctly diagnose the root cause and provide actionable documentation links for at least 80% of 30 curated slow-query benchmark test cases.
5. Implement `GET /health` responding with 200 OK for process liveness, and `GET /ready` verifying loaded records status and returning HTTP 503 if records count is 0.

## Non-Functional Requirements

1. Maintain a P95 response time under 50 milliseconds for `GET /health` and `GET /v1/documents` under a concurrency load of 20 requests per second.
2. Maintain 100% pass rate across a minimum of 6 automated integration tests with total execution time under 3 seconds.
3. Terminate process startup in under 1 second with a ValidationError if `APP_ENV` is unset or not matching `local`, `ci`, or `production`.
4. Format 100% of application log records as single-line JSON with standardized fields (`ts`, `level`, `logger`, `msg`, `request_id`, `duration_ms`).
5. Maintain zero errors and zero warnings under Ruff linting with target Python 3.12, strict rule sets (E, F, I, B, UP, SIM), and a line length limit of 100 characters.
