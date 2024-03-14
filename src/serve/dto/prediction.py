from pydantic import BaseModel


# Order of the fields is important for inverse transformation
class PredictBikesDTO(BaseModel):
    available_bike_stands: int
    surface_pressure: float
    temperature: float
    apparent_temperature: float
    relative_humidity: float


class PredictionDTO(BaseModel):
    prediction: int
