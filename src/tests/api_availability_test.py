from src.config import settings
from src.data.data_fetcher import DataFetcher


def test_mbajk_endpoint():
    fetcher = DataFetcher(lat=settings.lat, lon=settings.lon)
    stations = fetcher.get_bike_stations()
    assert len(stations) > 0


def test_weather_endpoint():
    fetcher = DataFetcher(lat=settings.lat, lon=settings.lon)
    weather = fetcher.get_weather_forecast()
    assert len(weather) > 0
