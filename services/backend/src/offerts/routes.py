from database.db import DB
from fastapi import APIRouter

router = APIRouter(prefix="/api/offerts")


@router.post("/leading")
def get_leading_offerts(
    offset: int = 0,
    limit: int = 20,
):
    return DB.get_leading_offerts(offset, limit)
