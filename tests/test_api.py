import pytest
from pydantic import ValidationError

from querydoctor.config import Settings
from querydoctor.db.url import to_asyncpg_url


def test_health_is_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ready_when_database_up(client):
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json()["checks"]["database"] is True


def test_ready_is_503_when_database_down(client, db_state):
    db_state["up"] = False
    assert client.get("/health").status_code == 200  # alive...
    assert client.get("/ready").status_code == 503  # ...but not ready


def test_list_documents_paginates(client):
    body = client.get("/v1/documents", params={"limit": 2}).json()
    assert body["total"] == 3
    assert len(body["items"]) == 2


def test_search_filters_records(client):
    r = client.get("/v1/documents", params={"q": "beta"})
    assert [d["id"] for d in r.json()["items"]] == ["002"]


def test_get_document_found(client):
    r = client.get("/v1/documents/001")
    assert r.status_code == 200
    assert r.json()["title"] == "Alpha guideline"


def test_missing_document_is_problem_details(client):
    r = client.get("/v1/documents/999")
    assert r.status_code == 404
    assert r.headers["content-type"] == "application/problem+json"
    body = r.json()
    assert body["status"] == 404
    assert body["title"] == "Not Found"
    assert body["request_id"] == r.headers["X-Request-ID"]


def test_bad_limit_is_422_problem(client):
    r = client.get("/v1/documents", params={"limit": 0})
    assert r.status_code == 422
    assert r.json()["errors"][0]["field"] == "query.limit"


def test_request_id_is_echoed(client):
    r = client.get("/health", headers={"X-Request-ID": "abc123"})
    assert r.headers["X-Request-ID"] == "abc123"


def test_app_refuses_to_start_without_app_env(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_bad_filter_key_returns_400(client):
    r = client.get("/v1/documents", params={"Bad-Name": "1"})
    assert r.status_code == 400
    assert r.headers["content-type"] == "application/problem+json"


def test_metadata_filter_applied(client):
    r = client.get("/v1/documents", params={"kind": "circular"})
    body = r.json()
    assert body["filters"] == {"kind": "circular"}
    assert all(d["kind"] == "circular" for d in body["items"])


def test_metadata_filter_numeric(client):
    r = client.get("/v1/documents", params={"year": "2024"})
    body = r.json()
    assert body["filters"] == {"year": "2024"}
    assert [d["id"] for d in body["items"]] == ["002"]


def test_url_converter_strips_sslmode():
    raw = "postgresql://u:p@h/d?sslmode=require&channel_binding=require"  # pragma: allowlist secret
    result = to_asyncpg_url(raw)
    assert "sslmode" not in result
    assert "channel_binding" not in result
    assert "ssl=require" in result
    assert result.startswith("postgresql+asyncpg://")


def test_url_converter_local_no_ssl():
    raw = "postgresql://localhost:5432/querydoctor"
    result = to_asyncpg_url(raw)
    assert result.startswith("postgresql+asyncpg://")
    assert "ssl" not in result


def test_offset_paginates_correctly(client):
    r1 = client.get("/v1/documents", params={"limit": 2, "offset": 0}).json()
    r2 = client.get("/v1/documents", params={"limit": 2, "offset": 2}).json()
    ids1 = [d["id"] for d in r1["items"]]
    ids2 = [d["id"] for d in r2["items"]]
    assert ids1 != ids2
    assert r1["total"] == r2["total"] == 3
