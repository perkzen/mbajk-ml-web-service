from pydantic import BaseModel

from .weather import Weather


class BikeStation(BaseModel):
    available_bike_stands: int
    available_bikes: int
    name: str
    address: str


class BikeStationWithWeather(BikeStation, Weather):
    pass
