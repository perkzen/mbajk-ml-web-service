import concurrent.futures
from src.config import MARIBOR_LAT, MARIBOR_LON
from src.utils.decorators import execution_timer
from ..data_fetcher import DataFetcher
from ..data_manager import DataManager


@execution_timer(name="Fetch Weather")
def get_current_weather(fetcher, manager):
    weather = fetcher.get_current_weather()
    weather = manager.create_dataframe(weather)
    manager.save("raw", "weather", weather)


@execution_timer(name="Fetch Bike Stations")
def get_bike_stations(fetcher, manager):
    stations = fetcher.get_bike_stations()
    stations = manager.create_dataframe(stations)
    manager.save("raw", "mbajk_stations", stations)


@execution_timer(name="Fetch Data")
def main() -> None:
    fetcher = DataFetcher(lat=MARIBOR_LAT, lon=MARIBOR_LON)
    manager = DataManager(data_path="data")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_weather = executor.submit(get_current_weather, fetcher, manager)
        future_stations = executor.submit(get_bike_stations, fetcher, manager)

        concurrent.futures.wait([future_weather, future_stations])


if __name__ == "__main__":
    main()
