import pandas as pd


class BikeStationsService:

    @staticmethod
    def get_bike_stations():
        df = pd.read_csv(f"data/raw/mbajk_stations.csv")
        return df.to_dict(orient="records")

    @staticmethod
    def get_bike_station_by_number(number: int):
        df = pd.read_csv("data/raw/mbajk_stations.csv")
        return df[df["number"] == number].to_dict(orient="records")[0]
