from typing import List
from fastapi import HTTPException, APIRouter
from src.config import WINDOW_SIZE
from src.serve.dto import PredictBikesDTO, PredictionDTO
from src.serve.services import MLService

router = APIRouter(
    prefix="/mbajk",
    tags=["mbajk"]
)

ml_service = MLService("mbajk_GRU_model", "minmax")


@router.post("/predict")
def predict(data: List[PredictBikesDTO]) -> PredictionDTO:
    if len(data) != WINDOW_SIZE:
        raise HTTPException(status_code=400, detail=f"Data must contain {WINDOW_SIZE} items")

    prediction = int(ml_service.predict(data))
    return PredictionDTO(prediction=prediction)
