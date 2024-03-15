from pydantic import BaseModel


# Order of the fields is important for inverse transformation
class PredictBikesDTO(BaseModel):
    available_bike_stands: int
    surface_pressure: float
    temperature: float
    apparent_temperature: float
    relative_humidity: float

    @classmethod
    def from_dataset(cls, dataset: dict):
        return cls(
            available_bike_stands=dataset["available_bike_stands"],
            surface_pressure=dataset["surface_pressure"],
            temperature=dataset["temperature"],
            apparent_temperature=dataset["apparent_temperature"],
            relative_humidity=dataset["relative_humidity"]
        )


class PredictionDTO(BaseModel):
    prediction: int
    date: str
