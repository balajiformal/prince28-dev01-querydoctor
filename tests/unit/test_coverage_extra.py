"""Extra unit tests for edge-case branch coverage across Days 1-9."""

import json
from datetime import date

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from querydoctor.api.middleware import request_context
from querydoctor.config import get_settings
from querydoctor.db.models import Document
from querydoctor.db.repository import _value_candidates, to_dict
from querydoctor.db.url import to_asyncpg_url
from querydoctor.ingest.store import document_id
from querydoctor.llm.doc_meta import DocMeta
from querydoctor.llm.extract import RESERVED, explain, extract, parse_json, run
from querydoctor.llm.gateway import FakeLLM, LLMError, LLMGateway, OpenAICompatProvider, Reply
from querydoctor.llm.prompts import latest, read_prompt, versions

# ---- D01-D02: Config, Middleware, URL ----


def test_get_settings_returns_cached_instance():
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2


def test_to_asyncpg_url_keeps_asyncpg_and_handles_ssl():
    already = "postgresql+asyncpg://u:p@host/db?sslmode=disable"
    assert to_asyncpg_url(already) == "postgresql+asyncpg://u:p@host/db"
    sync = "postgres://u:p@host/db?sslmode=require&channel_binding=require"
    assert to_asyncpg_url(sync) == "postgresql+asyncpg://u:p@host/db?ssl=require"


def test_middleware_turns_unhandled_exception_into_500_problem_json():
    app = FastAPI()
    app.middleware("http")(request_context)

    @app.get("/boom")
    async def boom():
        raise RuntimeError("unexpected crash")

    client = TestClient(app, raise_server_exceptions=False)
    r = client.get("/boom", headers={"X-Request-ID": "req-123"})
    assert r.status_code == 500
    assert r.headers["X-Request-ID"] == "req-123"
    assert r.json()["request_id"] == "req-123"
    assert r.json()["status"] == 500


# ---- D03: Repository & Models ----


def test_value_candidates_parses_types():
    assert _value_candidates("true") == ["true", ["true"], True]
    assert _value_candidates("false") == ["false", ["false"], False]
    assert _value_candidates("16") == ["16", ["16"], 16]
    assert _value_candidates("3.14") == ["3.14", ["3.14"], 3.14]
    assert _value_candidates("explain") == ["explain", ["explain"]]


def test_to_dict_serializes_document_with_and_without_published_on():
    doc = Document(
        external_id="doc-1",
        doc_type="html",
        title="Using EXPLAIN",
        source_url="https://www.postgresql.org/docs/current/using-explain.html",
        licence="PostgreSQL License",
        published_on=date(2024, 11, 1),
        metadata_={"doc_kind": "tutorial"},
    )
    out = to_dict(doc)
    assert out["id"] == "doc-1"
    assert out["doc_kind"] == "tutorial"
    assert out["published_on"] == "2024-11-01"

    doc.published_on = None
    assert to_dict(doc)["published_on"] is None


# ---- D07: Store helper ----


def test_document_id_uses_sha256_prefix():
    assert document_id("ab" * 32) == "f-" + ("ab" * 10)


# ---- D08: Gateway streaming transport error ----


@pytest.mark.asyncio
async def test_provider_stream_turns_transport_error_into_retryable_llm_error():
    def drops(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection reset")

    client = httpx.AsyncClient(transport=httpx.MockTransport(drops))
    provider = OpenAICompatProvider("gemini", "https://llm.test/v1/", "k", "m", client=client)
    with pytest.raises(LLMError) as err:
        async for _ in provider.stream([{"role": "user", "content": "hi"}], Reply()):
            pass
    assert err.value.retryable


# ---- D09: Prompts & Extract edge cases ----


def test_explain_handles_plain_value_error():
    assert explain(ValueError("bad input")) == "bad input"


def test_parse_json_extracts_nested_object():
    assert parse_json('prefix {"a": {"b": 1}} suffix') == {"a": {"b": 1}}


def test_doc_meta_fields_do_not_clash_with_reserved():
    assert not (RESERVED & set(DocMeta.model_fields))


def test_prompts_versions_sorting_and_missing(tmp_path):
    for name in ("task_v10", "task_v2", "task_v1"):
        (tmp_path / f"{name}.md").write_text(f"body {name}", encoding="utf-8")
    assert versions(tmp_path, "task") == ["task_v1", "task_v2", "task_v10"]
    assert latest(tmp_path, "task") == "task_v10"
    assert read_prompt(tmp_path, "task_v1") == "body task_v1"
    with pytest.raises(FileNotFoundError):
        latest(tmp_path, "missing")


@pytest.mark.asyncio
async def test_extract_native_schema_and_exhausted_attempts():
    valid = {
        "doc_kind": "reference",
        "year": None,
        "language": "en",
        "summary": "Reference documentation for PostgreSQL memory configuration.",
        "topics": ["memory"],
        "chapter": [],
        "version": [],
        "sql_command": [],
        "config_param": ["work_mem"],
    }
    llm = FakeLLM(script=[json.dumps(valid)])
    gw = LLMGateway([llm])
    res = await extract(
        gateway=gw,
        schema=DocMeta,
        prompt="Extract",
        version="extract_v1",
        title="Doc",
        text="Body",
        native_schema=True,
    )
    assert res.record is not None
    assert llm.seen[0]["response_format"]["type"] == "json_schema"

    llm_bad = FakeLLM(script=["not json", "still not json", "{}"])
    res_bad = await extract(
        gateway=LLMGateway([llm_bad]),
        schema=DocMeta,
        prompt="Extract",
        version="extract_v1",
        title="Doc",
        text="Body",
        max_attempts=3,
    )
    assert res_bad.record is None
    assert res_bad.attempts == 3
    assert len(res_bad.errors) == 3


@pytest.mark.asyncio
async def test_extract_run_rejects_reserved_field_name():
    class BadSchema(BaseModel):
        pages: int

    with pytest.raises(ValueError, match="already uses them"):
        await run(None, LLMGateway([]), BadSchema, "Extract", "extract_v1")  # type: ignore[arg-type]


def test_info_and_classify_and_facets_endpoints(client, llm):
    r_info = client.get("/info")
    assert r_info.status_code == 200 and r_info.json()["docs_url"] == "/docs"

    llm.script = ["docs"]
    r_cls = client.post("/v1/classify", json={"message": "What is work_mem?"})
    assert r_cls.status_code == 200
    assert r_cls.json()["label"] == "docs"
    assert r_cls.json()["prompt_version"].startswith("classify_v")
