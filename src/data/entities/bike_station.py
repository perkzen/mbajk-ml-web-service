from pydantic import BaseModel


class BikeStation(BaseModel):
    available_bike_stands: int
    available_bikes: int
    name: str
    address: str


class BikeStationWithWeather(BaseModel):
    # Weather
    date: str
    temperature: float
    relative_humidity: float
    dew_point: float
    apparent_temperature: float
    precipitation: float
    rain: float
    surface_pressure: float

    # BikeStation
    name: str
    address: str
    available_bike_stands: int
    available_bikes: int


