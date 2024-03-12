from typing import List
from fastapi import FastAPI, HTTPException
from datetime import datetime
from .dto.predict_bikes_dto import BikeStationDto
from .services.bike_stations_service import BikeStationsService
from .services.ml_service import MLService
from ..config import WINDOW_SIZE
from ..data.entities import BikeStation

app = FastAPI()

ml_service = MLService("mbajk_GRU_model", "minmax")
bike_stations_service = BikeStationsService()


@app.get("/")
def health_check():
    date = datetime.now()
    return {"status": "ok", "date": date}


@app.get("/mbjak/stations")
def get_bike_stations() -> List[BikeStation]:
    return bike_stations_service.get_bike_stations()


@app.get("/mbjak/stations/{number}")
def get_bike_station_by_number(number: int) -> BikeStation:
    return bike_stations_service.get_bike_station_by_number(number)


@app.post("/mbjak/predict")
def predict(data: List[BikeStationDto]):
    if len(data) != WINDOW_SIZE:
        raise HTTPException(status_code=400, detail=f"Data must contain {WINDOW_SIZE} items")

    prediction = int(ml_service.predict(data))
    return {"prediction": prediction}
