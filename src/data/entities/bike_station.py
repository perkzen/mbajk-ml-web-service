from pydantic import BaseModel


class BikeStation(BaseModel):
    available_bike_stands: int
    available_bikes: int
    bike_stands: int
    name: str
    address: str
    number: int
