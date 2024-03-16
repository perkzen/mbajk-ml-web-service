from typing import List
from src.config import settings
from src.data.data_fetcher import DataFetcher
from src.data.entities import BikeStation
from src.serve.dto import BikeStationDTO


class BikeStationsService:

    def __init__(self):
        self.fetcher = DataFetcher(lat=settings.lat, lon=settings.lon)

    def get_bike_stations(self) -> List[BikeStationDTO]:
        stations: List[BikeStation] = self.fetcher.get_bike_stations()
        return [BikeStationDTO.from_entity(station) for station in stations]

    def get_bike_station_by_number(self, number: int):
        station: BikeStation = self.fetcher.get_bike_station(number)
        return BikeStationDTO.from_entity(station)
