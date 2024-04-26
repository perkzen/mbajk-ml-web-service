from typing import List
from fastapi import APIRouter, HTTPException
from src.serve.dto import PredictionDTO
from src.serve.services import MLService, BikeStationsService
from src.serve.services.prediction_service import PredictionService
from cachetools import TTLCache

router = APIRouter(
    prefix="/mbajk",
    tags=["mbajk"]
)

bike_service = BikeStationsService()

# Create a cache with a TTL (time-to-live) of 1 hour (3600 seconds)
cache = TTLCache(maxsize=1000, ttl=3600)


@router.get("/predict/{station_number}/{n_future}")
def predict_multiple(station_number: int, n_future: int) -> List[PredictionDTO]:
    if n_future < 1:
        raise HTTPException(status_code=400, detail="n_future must be greater than 0")

    if n_future > 7:
        raise HTTPException(status_code=400, detail="n_future must be less than 8")

    if station_number < 0 or station_number > 29:
        raise HTTPException(status_code=400, detail="station_number must be between 0 and 28")

    cache_key = (station_number, n_future)
    if cache_key in cache:
        return cache[cache_key]

    data = bike_service.get_bike_station_history_data(station_number)

    ml_service = MLService(f"{station_number}/model", f"{station_number}/minmax")

    predictions = ml_service.predict_multiple(data, n_future)

    PredictionService.save(station_number, n_future, predictions)

    cache[cache_key] = predictions

    return predictions
