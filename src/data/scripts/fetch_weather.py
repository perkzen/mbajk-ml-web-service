from src.config import settings
from src.data.data_fetcher import DataFetcher
from src.data.data_manager import DataManager
from src.utils.decorators import execution_timer


@execution_timer(name="Fetch Weather")
def main() -> None:
    fetcher = DataFetcher(lat=settings.lat, lon=settings.lon)
    manager = DataManager(data_path="data")

    weather = fetcher.get_current_weather()
    weather = manager.create_dataframe(weather)
    manager.save("raw", "weather", weather)


if __name__ == "__main__":
    main()
