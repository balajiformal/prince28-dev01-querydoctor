import json

import pytest
from pydantic import ValidationError

from querydoctor.llm.doc_meta import DocMeta
from querydoctor.llm.extract import explain, extract, parse_json
from querydoctor.llm.gateway import FakeLLM, LLMGateway


def test_parse_json_simple():
    assert parse_json('{"key": "value"}') == {"key": "value"}


def test_parse_json_wrapped_in_markdown():
    reply = 'Here is the result:\n```json\n{"doc_kind": "guide"}\n```\nHope it helps!'
    assert parse_json(reply) == {"doc_kind": "guide"}


def test_parse_json_invalid():
    with pytest.raises(ValueError, match="no JSON object"):
        parse_json("No json here")

    with pytest.raises(ValueError, match="no JSON object"):
        parse_json("[1, 2, 3]")

    with pytest.raises(json.JSONDecodeError):
        parse_json("{invalid_json: 123}")


def test_doc_meta_valid():
    meta = DocMeta(
        doc_kind="reference",
        year=2024,
        language="en",
        summary="A comprehensive reference guide for PostgreSQL EXPLAIN plans and execution costs.",
        topics=["Postgres", "EXPLAIN", "postgres"],
        chapter=["Performance Tips"],
        version=["16", "17"],
        sql_command=["EXPLAIN"],
        config_param=["enable_seqscan"],
    )
    assert meta.doc_kind == "reference"
    # Deduplicated and lowercased
    assert meta.topics == ["postgres", "explain"]
    assert meta.year == 2024
    assert meta.chapter == ["Performance Tips"]


def test_doc_meta_invalid_extra_field():
    with pytest.raises(ValidationError):
        DocMeta(
            doc_kind="reference",
            language="en",
            summary="This is a valid length summary of the document for testing purposes.",
            topics=["postgres"],
            chapter=[],
            version=[],
            sql_command=[],
            config_param=[],
            extra_field="disallowed",
        )


def test_explain_validation_error():
    try:
        DocMeta(
            doc_kind="invalid_kind",  # type: ignore
            language="en",
            summary="Too short",
            topics=[],
            chapter=[],
            version=[],
            sql_command=[],
            config_param=[],
        )
    except ValidationError as err:
        msg = explain(err)
        assert "doc_kind" in msg or "summary" in msg


@pytest.mark.asyncio
async def test_extract_success():
    valid_data = {
        "doc_kind": "tutorial",
        "year": 2023,
        "language": "en",
        "summary": "Detailed guide on using EXPLAIN ANALYZE for query optimization in Postgres.",
        "topics": ["performance", "explain"],
        "chapter": ["Using EXPLAIN"],
        "version": ["15"],
        "sql_command": ["EXPLAIN"],
        "config_param": [],
    }
    llm = FakeLLM(script=[json.dumps(valid_data)])
    gw = LLMGateway([llm])

    res = await extract(
        gateway=gw,
        schema=DocMeta,
        prompt="Extract metadata",
        version="v1",
        title="Using EXPLAIN",
        text="Content of doc from 2023",
    )
    assert res.record is not None
    assert isinstance(res.record, DocMeta)
    assert res.record.doc_kind == "tutorial"
    assert res.attempts == 1
    assert len(res.errors) == 0


@pytest.mark.asyncio
async def test_extract_rejects_hallucinated_year():
    bad_year = {
        "doc_kind": "tutorial",
        "year": 2024,
        "language": "en",
        "summary": "Detailed guide on using EXPLAIN ANALYZE for query optimization in Postgres.",
        "topics": ["performance", "explain"],
        "chapter": ["Using EXPLAIN"],
        "version": ["15"],
        "sql_command": ["EXPLAIN"],
        "config_param": [],
    }
    good = {**bad_year, "year": None}
    llm = FakeLLM(script=[json.dumps(bad_year), json.dumps(good)])
    gw = LLMGateway([llm])

    res = await extract(
        gateway=gw,
        schema=DocMeta,
        prompt="Extract metadata",
        version="v1",
        title="Using EXPLAIN",
        text="Content of doc with no year mentioned.",
    )
    assert res.record is not None
    assert res.record.year is None
    assert res.attempts == 2
    assert "year 2024 is not in the document" in res.errors[0]


def test_the_extract_prompt_names_every_field_of_the_contract():
    from pathlib import Path

    from querydoctor.llm.prompts import latest, read_prompt

    prompt = read_prompt(Path("prompts"), latest(Path("prompts"), "extract"))
    missing = [name for name in DocMeta.model_fields if name not in prompt]
    assert not missing, f"prompts/extract_v*.md does not mention: {missing}"


@pytest.mark.asyncio
async def test_extract_repair_loop():
    # First response is invalid JSON; second response is valid DocMeta
    invalid_data = "{'invalid_json': true"
    valid_data = {
        "doc_kind": "rule",
        "year": None,
        "language": "en",
        "summary": "Guidelines and rules for database vacuuming and transaction ID wraparound.",
        "topics": ["vacuum"],
        "chapter": ["Routine Vacuuming"],
        "version": ["17"],
        "sql_command": ["VACUUM"],
        "config_param": ["autovacuum_max_workers"],
    }
    llm = FakeLLM(script=[invalid_data, json.dumps(valid_data)])
    gw = LLMGateway([llm])

    res = await extract(
        gateway=gw,
        schema=DocMeta,
        prompt="Extract metadata",
        version="v1",
        title="Vacuum",
        text="Content of doc",
    )
    assert res.record is not None
    assert res.attempts == 2
    assert len(res.errors) == 1
