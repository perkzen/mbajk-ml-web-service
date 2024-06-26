from typing import List
from datetime import datetime
import requests
from .entities import BikeStation, Weather
from ..config import settings
import pytz


class DataFetcher:
    stations_url = ("https://api.jcdecaux.com/vls/v1/stations?contract=maribor&"
                    f"apiKey={settings.mbajk_api_key}")

    weather_base_url = "https://archive-api.open-meteo.com/v1/archive?"

    timezone = pytz.timezone('Europe/Berlin')

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def get_bike_stations(self):
        stations_response = requests.get(self.stations_url)
        stations_response.raise_for_status()

        stations = stations_response.json()

        now = datetime.now(self.timezone).strftime('%Y-%m-%dT%H:00:00')

        return [
            BikeStation(
                available_bike_stands=station["available_bike_stands"],
                available_bikes=station["available_bikes"],
                bike_stands=station["bike_stands"],
                name=station["name"],
                address=station["address"],
                number=station["number"],
                date=now,
                lat=station["position"]["lat"],
                lon=station["position"]["lng"],
                last_updated=station["last_update"]
            )
            for station in stations
        ]

    def get_weather_forecast(self, days: int = 2) -> List[Weather]:
        weather_url = self.__create_forecast_url(forecast_days=days)
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()

        parsed_data = self.__parse_forecast_response(weather_response.json())

        return self.__map_to_weather_data(parsed_data)

    def get_weather_forecast_for_next_n_hours(self, hours: int = 1) -> List[Weather]:
        now = datetime.now(self.timezone)
        current_hour = now.hour

        measurements_in_one_day = 24
        n_future_days = max(1, (current_hour + hours) // measurements_in_one_day) + 1  # +1 for the current day
        weather = self.get_weather_forecast(days=n_future_days)

        now = datetime.now(self.timezone).strftime('%Y-%m-%dT%H:00')

        return [w for w in weather if w.date > now][:hours]

    def get_current_weather(self) -> Weather:
        date_hour = datetime.now(self.timezone).strftime('%Y-%m-%dT%H:00')

        weather = self.get_weather_forecast()

        for w in weather:
            if w.date == date_hour:
                now = datetime.now(self.timezone).strftime('%Y-%m-%dT%H:00:00')
                w.date = now
                return w

    def get_bike_station(self, number: int) -> BikeStation:
        stations = self.get_bike_stations()
        for station in stations:
            if station.number == number:
                return station

    def __create_forecast_url(self, past_days: int = 0, forecast_days: int = 1):
        base_url = "https://api.open-meteo.com/v1/forecast?"
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "hourly": "temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation,"
                      "surface_pressure,rain",
            "past_days": past_days,
            "forecast_days": forecast_days
        }
        forecast_url = base_url + "&".join([f"{key}={value}" for key, value in params.items()])
        return forecast_url

    @staticmethod
    def __parse_forecast_response(response: dict):
        data = {'latitude': response['latitude'], 'longitude': response['longitude'], 'hourly': {}}

        for key, values in response['hourly'].items():
            data['hourly'][key] = values

        return data

    @staticmethod
    def __map_to_weather_data(parsed_data: dict) -> List[Weather]:
        weather_data_list = []
        for i in range(len(parsed_data['hourly']['time'])):
            weather_data = Weather(
                temperature=parsed_data['hourly']['temperature_2m'][i],
                relative_humidity=parsed_data['hourly']['relative_humidity_2m'][i],
                dew_point=parsed_data['hourly']['dew_point_2m'][i],
                apparent_temperature=parsed_data['hourly']['apparent_temperature'][i],
                precipitation=parsed_data['hourly']['precipitation'][i],
                rain=parsed_data['hourly']['rain'][i],
                surface_pressure=parsed_data['hourly']['surface_pressure'][i],
                date=parsed_data['hourly']['time'][i]
            )
            weather_data_list.append(weather_data)
        return weather_data_list
