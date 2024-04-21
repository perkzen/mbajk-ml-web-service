import os

from src.data.data_manager import DataManager
from src.utils.decorators import execution_timer


@execution_timer("Split Data")
def main():
    dm = DataManager(data_path="data")

    folders = [f for f in os.listdir("data/processed") if os.path.isdir(f"data/processed/{f}")]

    for folder in folders:
        station = dm.get_dataframe(f"processed/{folder}", f"mbajk_station_{folder}")

        station.drop("date", axis=1, inplace=True)

        test_size = int(0.1 * len(station))
        test_data = station.head(test_size)
        train_data = station.iloc[test_size:]

        dm.save(f"processed/{folder}", "train", train_data, override=True)
        dm.save(f"processed/{folder}", "test", test_data, override=True)
        print(f"[Station {folder}]: Train data shape: {train_data.shape}")
        print(f"[Station {folder}]: Test data shape: {test_data.shape}")


if __name__ == "__main__":
    main()
