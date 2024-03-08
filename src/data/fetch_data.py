import requests
from pydantic import BaseModel

stations_url = ("https://api.jcdecaux.com/vls/v1/stations?contract=maribor&"
                "apiKey=5e150537116dbc1786ce5bec6975a8603286526b")


class BikeStation(BaseModel):
    available_bike_stands: int
    available_bikes: int
    name: str
    address: str


def fetch_stations():
    response = requests.get(stations_url)
    response.raise_for_status()

    stations = response.json()

    return [
        BikeStation(
            available_bike_stands=station["available_bike_stands"],
            available_bikes=station["available_bikes"],
            name=station["name"],
            address=station["address"]
        )
        for station in stations
    ]


if __name__ == "__main__":
    print(fetch_stations()[:5])
