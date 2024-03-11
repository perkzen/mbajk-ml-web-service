import signal
import sys
import time
import schedule
from datetime import datetime
from ..data_fetcher import DataFetcher
from ..dataset_manager import DatasetManager


def signal_handler(_sig, _frame):
    print("Shutting down...")
    schedule.clear()
    time.sleep(1)
    sys.exit(0)


def task(data_fetcher: DataFetcher, dataset_manager: DatasetManager):
    start_time = datetime.now()

    print(f"[Task]: Fetching bike stations - {start_time.strftime('%Y-%m-%dT%H:%M')}", )

    stations = data_fetcher.get_stations_with_weather()

    for station in stations:
        df = dataset_manager.save("raw", station)

        if len(df) > 3:
            df = dataset_manager.clean(df)
            dataset_manager.save_df(df, "processed", station.name)

    end_time = datetime.now()
    execution_time = end_time - start_time

    print(f"[Task]: Fetch script executed in {int(execution_time.microseconds / 1000)}ms", )


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    fetcher = DataFetcher(lat=46.5547, lon=15.6467)
    manager = DatasetManager(data_path="data")

    schedule.every(1).seconds.do(task, fetcher, manager)

    while True:
        schedule.run_pending()
