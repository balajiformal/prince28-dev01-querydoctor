from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request

from querydoctor.api.deps import RepoDep
from querydoctor.api.errors import problem_response
from querydoctor.db.repository import FILTER_KEY

router = APIRouter(prefix="/documents", tags=["documents"])

# Query param names that are reserved for pagination / search, not metadata filters
RESERVED = {"q", "limit", "offset"}


@router.get("")
async def list_documents(
    request: Request,
    repo: RepoDep,
    q: Annotated[str | None, Query(max_length=200)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> dict:
    # Collect any extra query params as metadata filters
    filters: dict[str, str] = {}
    bad_keys: list[str] = []
    for key, value in request.query_params.items():
        if key in RESERVED:
            continue
        if not FILTER_KEY.match(key):
            bad_keys.append(key)
        else:
            filters[key] = value

    if bad_keys:
        return problem_response(request, 400, f"Invalid filter key(s): {bad_keys}")

    total, rows = await repo.list(q=q, filters=filters, limit=limit, offset=offset)
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "filters": filters,
        "items": rows,
    }


@router.get("/facets")
async def document_facets(repo: RepoDep) -> dict:
    """Distribution of extracted doc_kind and language values."""
    return await repo.facets()


@router.get("/{doc_id}")
async def get_document(doc_id: str, repo: RepoDep) -> dict:
    record = await repo.get(doc_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"No document with id '{doc_id}'.")
    return record
