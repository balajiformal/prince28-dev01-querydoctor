"""Integration test for metadata extraction and persistence."""

import pytest
from sqlalchemy import select

from querydoctor.config import Settings
from querydoctor.db.models import Document, Page
from querydoctor.db.session import make_engine, make_sessionmaker
from querydoctor.llm.doc_meta import DocMeta
from querydoctor.llm.extract import Extraction, pending, save


@pytest.fixture
async def session(database_url):
    engine = make_engine(Settings(app_env="ci", database_url=database_url, _env_file=None))
    async with make_sessionmaker(engine)() as db:
        await db.execute(Page.__table__.delete())
        await db.execute(Document.__table__.delete())
        await db.commit()
        yield db
    await engine.dispose()


async def test_extract_metadata_stored_in_postgres(session):
    # Setup document
    doc = Document(
        external_id="test_doc_001",
        doc_type="html",
        title="Using EXPLAIN",
        metadata_={"source": "postgres-docs", "pages": 1},
    )
    session.add(doc)
    await session.commit()
    await session.refresh(doc)

    # Check pending
    todo = await pending(session, version="v1")
    assert len(todo) == 1
    assert todo[0].id == doc.id

    # Save extraction
    meta = DocMeta(
        doc_kind="tutorial",
        year=2024,
        language="en",
        summary="Detailed guide on using EXPLAIN and EXPLAIN ANALYZE in PostgreSQL.",
        topics=["performance", "explain"],
        chapter=["Using EXPLAIN"],
        version=["16"],
        sql_command=["EXPLAIN"],
        config_param=[],
    )
    extraction = Extraction(
        record=meta,
        attempts=1,
        model="fake-model",
        tokens_in=100,
        tokens_out=50,
        cost_inr=0.02,
    )
    await save(session, doc, extraction, version="v1")

    # Verify updated metadata
    saved = await session.scalar(select(Document).where(Document.id == doc.id))
    assert saved.metadata_["doc_kind"] == "tutorial"
    assert saved.metadata_["topics"] == ["performance", "explain"]
    assert saved.metadata_["extract"]["prompt"] == "v1"
    assert saved.metadata_["extract"]["attempts"] == 1

    # Now pending should be empty
    todo_after = await pending(session, version="v1")
    assert len(todo_after) == 0
