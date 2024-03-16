from fastapi import APIRouter
from datetime import datetime


router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("")
def health_check():
    date = datetime.now()
    return {"status": "ok", "date": date}
