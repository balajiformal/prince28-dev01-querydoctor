"""Extra unit tests for edge-case branch coverage across repository, prompts, and extract."""

import pytest

from querydoctor.db.repository import _value_candidates
from querydoctor.llm.doc_meta import DocMeta
from querydoctor.llm.extract import RESERVED, explain, extract
from querydoctor.llm.gateway import FakeLLM, LLMGateway
from querydoctor.llm.prompts import latest, read_prompt, versions


def test_value_candidates_parses_types():
    assert _value_candidates("true") == ["true", ["true"], True]
    assert _value_candidates("false") == ["false", ["false"], False]
    assert _value_candidates("16") == ["16", ["16"], 16]
    assert _value_candidates("3.14") == ["3.14", ["3.14"], 3.14]
    assert _value_candidates("explain") == ["explain", ["explain"]]


def test_explain_handles_plain_value_error():
    assert explain(ValueError("bad input")) == "bad input"


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
async def test_extract_exhausts_max_attempts():
    llm = FakeLLM(script=["not json", "still not json", "{}"])
    gw = LLMGateway([llm])
    res = await extract(
        gateway=gw,
        schema=DocMeta,
        prompt="Extract",
        version="extract_v1",
        title="Doc",
        text="Body",
        max_attempts=3,
    )
    assert res.record is None
    assert res.attempts == 3
    assert len(res.errors) == 3
