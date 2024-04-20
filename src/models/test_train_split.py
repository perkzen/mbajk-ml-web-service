from typing import Tuple

import pandas as pd

from src.data.data_manager import DataManager


def create_test_train_split(folder: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    dm = DataManager(data_path="data/processed")
    train_data = dm.get_dataframe(folder=folder, file_name="train")
    test_data = dm.get_dataframe(folder=folder, file_name="test")

    return train_data, test_data
