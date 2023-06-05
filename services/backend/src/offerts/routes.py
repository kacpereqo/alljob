from database.db import DB
from fastapi import APIRouter

router = APIRouter(prefix="/api/offerts")


@router.post("/leading")
def get_leading_offerts():
    return DB.get_leading_offerts()
