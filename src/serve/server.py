from typing import List
from fastapi import FastAPI, HTTPException
from datetime import datetime
from .dto.bike_station_dto import BikeStationDto
from .services.ml_service import MLService
from ..config import WINDOW_SIZE

app = FastAPI()

ml_service = MLService("mbajk_GRU_model", "minmax")


@app.get("/")
def health_check():
    date = datetime.now()
    return {"status": "ok", "date": date}


@app.post("/mbjak/predict")
def predict(data: List[BikeStationDto]):
    if len(data) != WINDOW_SIZE:
        raise HTTPException(status_code=400, detail=f"Data must contain {WINDOW_SIZE} items")

    prediction = int(ml_service.predict(data))
    return {"prediction": prediction}
