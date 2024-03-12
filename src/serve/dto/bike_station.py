from pydantic import BaseModel

from src.data.entities import BikeStation


class BikeStationDTO(BaseModel):
    available_bike_stands: int
    available_bikes: int
    bike_stands: int
    name: str
    address: str
    number: int
    date: str

    @classmethod
    def from_entity(cls, entity: BikeStation):
        return cls(
            available_bike_stands=entity.available_bike_stands,
            available_bikes=entity.available_bikes,
            bike_stands=entity.bike_stands,
            name=entity.name,
            address=entity.address,
            number=entity.number,
            date=entity.date,
        )
