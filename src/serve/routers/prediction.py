from typing import List

from fastapi import APIRouter, HTTPException

from src.serve.dto import PredictionDTO
from src.serve.services import MLService, DataService
from src.serve.services.prediction_service import PredictionService

router = APIRouter(
    prefix="/mbajk",
    tags=["mbajk"]
)

data_service = DataService()


@router.get("/predict/{station_number}/{n_future}")
def predict_multiple(station_number: int, n_future: int) -> List[PredictionDTO]:
    if n_future < 1:
        raise HTTPException(status_code=400, detail="n_future must be greater than 0")

    if station_number < 0 or station_number > 28:
        raise HTTPException(status_code=400, detail="station_number must be between 0 and 28")

    data = data_service.get_latest_data(station_number)
    ml_service = MLService(f"{station_number}/model", f"{station_number}/minmax")
    predictions = ml_service.predict_multiple(data, n_future)

    PredictionService.save(station_number, n_future, predictions)

    return predictions
