from typing import List

from fastapi import APIRouter

from src.serve.dto import BikeStationDTO
from src.serve.services import BikeStationsService

router = APIRouter(
    prefix="/mbajk/stations",
    tags=["mbajk"]
)

bike_stations_service = BikeStationsService()


@router.get("")
def get_bike_stations() -> List[BikeStationDTO]:
    return bike_stations_service.get_bike_stations()


@router.get("/{number}")
def get_bike_station_by_number(number: int) -> BikeStationDTO:
    return bike_stations_service.get_bike_station_by_number(number)
