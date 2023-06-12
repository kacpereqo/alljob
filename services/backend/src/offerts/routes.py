from database.db import DB
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from offerts.schemas import Filtering, Sorting

router = APIRouter(prefix="/api/offerts")


@router.post("/leading")
def get_leading_offerts(
    offset: int = 0,
    limit: int = 20,
    sorting: Sorting | None = None,
    filters: Filtering | None = None,
) -> JSONResponse:
    return DB.get_leading_offerts(offset, limit, sorting, filters)


@router.get("/details/{offert_id}")
def get_offert_details(offert_id: str) -> JSONResponse:
    return DB.get_offert_details(offert_id)
