from src.config import MARIBOR_LAT, MARIBOR_LON
from src.utils.decorators import execution_timer
from ..data_fetcher import DataFetcher
from ..data_manager import DataManager


@execution_timer("Fetch Data")
def main() -> None:
    fetcher = DataFetcher(lat=MARIBOR_LAT, lon=MARIBOR_LON)
    manager = DataManager(data_path="data")

    weather = fetcher.get_current_weather()
    weather = manager.create_dataframe(weather)
    manager.save("raw", "weather", weather)

    stations = fetcher.get_bike_stations()
    stations = manager.create_dataframe(stations)
    manager.save("raw", "mbajk_stations", stations)


if __name__ == "__main__":
    main()
