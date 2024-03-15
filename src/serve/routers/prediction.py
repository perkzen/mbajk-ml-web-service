from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException, APIRouter
from src.config import WINDOW_SIZE
from src.serve.dto import PredictBikesDTO, PredictionDTO
from src.serve.services import MLService, DataService

router = APIRouter(
    prefix="/mbajk",
    tags=["mbajk"]
)

ml_service = MLService("mbajk_GRU_model", "minmax")
data_service = DataService()


@router.post("/predict")
def predict(data: List[PredictBikesDTO]) -> PredictionDTO:
    if len(data) != WINDOW_SIZE:
        raise HTTPException(status_code=400, detail=f"Data must contain {WINDOW_SIZE} items")

    prediction = int(ml_service.predict(data))

    current_datetime = datetime.now()
    one_hour_later = current_datetime + timedelta(hours=1)
    date_str = one_hour_later.strftime('%Y-%m-%dT%H:00')

    return PredictionDTO(prediction=prediction, date=date_str)


@router.get("/predict/{n_future}")
def predict_multiple(n_future: int) -> List[PredictionDTO]:
    data = data_service.get_latest_data()
    predictions = ml_service.predict_multiple(data, n_future)
    return predictions
