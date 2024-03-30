from src.config import settings
from src.data.data_fetcher import DataFetcher
from src.data.data_manager import DataManager
from src.utils.decorators import execution_timer


@execution_timer(name="Fetch Bike Stations")
def main() -> None:
    fetcher = DataFetcher(lat=settings.lat, lon=settings.lon)
    manager = DataManager(data_path="data")

    stations = fetcher.get_bike_stations()
    stations = manager.create_dataframe(stations)
    manager.save("raw", "mbajk_stations", stations)


if __name__ == "__main__":
    main()
