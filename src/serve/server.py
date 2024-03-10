from typing import List
from fastapi import FastAPI, HTTPException
from datetime import datetime
from .dto.bike_station_dto import BikeStationDto
from .services.ml_service import MLService

app = FastAPI()

ml_service = MLService("mbajk_GRU_model", "minmax")


@app.get("/")
def health_check():
    date = datetime.now()
    return {"status": "ok", "date": date}


@app.post("/mbjak/predict")
def predict(data: List[BikeStationDto]):
    # 50 is window size (we should write it in a config file
    if len(data) != 50:
        raise HTTPException(status_code=400, detail="Data must contain 50 items")

    prediction = int(ml_service.predict(data))
    return {"prediction": prediction}
