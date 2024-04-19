from src.data.data_manager import DataManager
from src.utils.decorators import execution_timer


@execution_timer("Split Data")
def main():
    dm = DataManager(data_path="data")

    current = dm.get_dataframe("processed", "current_data")

    test_size = int(0.1 * len(current))

    test_data = current.head(test_size)
    train_data = current.iloc[test_size:]

    dm.save("processed", "train", train_data, override=True)
    dm.save("processed", "test", test_data, override=True)


if __name__ == "__main__":
    main()
