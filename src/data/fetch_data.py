import requests

stations_url = ("https://api.jcdecaux.com/vls/v1/stations?contract=maribor&"
                "apiKey=5e150537116dbc1786ce5bec6975a8603286526b")


def fetch_stations():
    response = requests.get(stations_url)
    response.raise_for_status()
    return response.json()
