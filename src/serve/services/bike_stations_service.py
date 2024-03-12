from typing import List
from src.config import MARIBOR_LAT, MARIBOR_LON
from src.data.data_fetcher import DataFetcher
from src.data.entities import BikeStation


class BikeStationsService:

    def __init__(self):
        self.fetcher = DataFetcher(lat=MARIBOR_LAT, lon=MARIBOR_LON)

    def get_bike_stations(self) -> List[BikeStation]:
        return self.fetcher.get_bike_stations()

    def get_bike_station_by_number(self, number: int) -> BikeStation:
        return self.fetcher.get_bike_station(number)
