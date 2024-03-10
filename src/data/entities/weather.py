from pydantic import BaseModel


class Weather(BaseModel):
    temperature: float
    relative_humidity: float
    dew_point: float
    apparent_temperature: float
    precipitation: float
    rain: float
    surface_pressure: float
    date: str

