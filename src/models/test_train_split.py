from typing import Tuple

import pandas as pd


def create_test_train_split(dataset: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    test_split = round(len(dataset) * 0.1)
    train_data = dataset[:-test_split]
    test_data = dataset[-test_split:]

    return train_data, test_data
