import asyncio
import os
import uuid

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from querydoctor.db.models import Document
from querydoctor.db.repository import DocumentRepository
from querydoctor.db.url import to_asyncpg_url

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not TEST_DATABASE_URL, reason="TEST_DATABASE_URL not set")


def test_db_connection():
    async def _test():
        engine = create_async_engine(to_asyncpg_url(TEST_DATABASE_URL))
        async with engine.connect() as conn:
            result = await conn.scalar(text("SELECT 1"))
            assert result == 1
        await engine.dispose()

    asyncio.run(_test())


def test_repo_insert_and_get():
    async def _test():
        engine = create_async_engine(to_asyncpg_url(TEST_DATABASE_URL))
        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        ext_id = f"test_{uuid.uuid4().hex[:8]}"
        async with session_factory() as session, session.begin():
            doc = Document(
                external_id=ext_id,
                title="Integration Test Document",
                doc_type="test",
                sha256="fake_sha256",
                metadata_={"tag": "integration", "number": 42},
            )
            session.add(doc)

        async with session_factory() as session:
            repo = DocumentRepository(session)
            fetched = await repo.get(ext_id)
            assert fetched is not None
            assert fetched["id"] == ext_id
            assert fetched["title"] == "Integration Test Document"
            assert fetched["tag"] == "integration"
        await engine.dispose()

    asyncio.run(_test())


def test_repo_metadata_filter():
    async def _test():
        engine = create_async_engine(to_asyncpg_url(TEST_DATABASE_URL))
        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        ext_id = f"test_{uuid.uuid4().hex[:8]}"
        unique_tag = f"tag_{uuid.uuid4().hex[:6]}"
        async with session_factory() as session, session.begin():
            doc = Document(
                external_id=ext_id,
                title="Filter Test Document",
                doc_type="test",
                sha256="fake_sha256_2",
                metadata_={"unique_tag": unique_tag},
            )
            session.add(doc)

        async with session_factory() as session:
            repo = DocumentRepository(session)
            total, items = await repo.list(
                q=None, filters={"unique_tag": unique_tag}, limit=10, offset=0
            )
            assert total >= 1
            assert any(item["id"] == ext_id for item in items)
        await engine.dispose()

    asyncio.run(_test())
