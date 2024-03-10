import signal
import sys
import time
import schedule
import pandas as pd
from datetime import datetime

from data_fetcher import DataFetcher


def signal_handler(_sig, _frame):
    print("Shutting down...")
    schedule.clear()
    time.sleep(1)
    sys.exit(0)


def task(data_fetcher: DataFetcher):
    start_time = datetime.now()

    print(f"[Task]: Fetching bike stations - {start_time.strftime('%Y-%m-%dT%H:MM')}", )

    stations = data_fetcher.get_stations_with_weather()

    stations = [station.dict() for station in stations]

    df = pd.DataFrame(stations)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    df.to_csv(f"data/raw/mbajk_dataset_{timestamp}.csv", index=False)

    end_time = datetime.now()
    execution_time = end_time - start_time

    print(f"[Task]: Fetch script executed in {int(execution_time.microseconds / 1000)}ms", )


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    fetcher = DataFetcher(lat=46.5547, lon=15.6467)

    schedule.every(1).hour.do(task, fetcher)

    while True:
        schedule.run_pending()
