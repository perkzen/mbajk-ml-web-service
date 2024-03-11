from src.utils.decorators import execution_timer
from ..data_fetcher import DataFetcher
from ..data_manager import DataManager


@execution_timer("Fetch Data")
def main() -> None:
    fetcher = DataFetcher(lat=46.5547, lon=15.6467)
    manager = DataManager(data_path="data")

    weather = fetcher.get_current_weather()
    weather = manager.create_dataframe(weather)
    manager.save("raw", "weather", weather)

    stations = fetcher.get_stations()
    stations = manager.create_dataframe(stations)
    manager.save("raw", "mbajk_stations", stations, True)


if __name__ == "__main__":
    main()
