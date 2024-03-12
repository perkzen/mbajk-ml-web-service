import pandas as pd


class BikeStationsService:

    def get_bike_stations(self):
        stations = self.__load_data()
        return stations.to_dict(orient="records")

    def get_bike_station_by_number(self, number: int):
        stations = self.__load_data()
        return stations[stations["number"] == number].to_dict(orient="records")[-1]

    @staticmethod
    def __load_data():
        return pd.read_csv("data/raw/mbajk_stations.csv")
