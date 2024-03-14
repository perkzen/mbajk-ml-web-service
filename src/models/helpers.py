import numpy as np
import pandas as pd
from typing import Tuple, Any
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
from sklearn.preprocessing import MinMaxScaler
from src.config import WINDOW_SIZE
from src.models import create_time_series, create_test_train_split


def load_dataset() -> pd.DataFrame:
    dataset = pd.read_csv("data/processed/mbajk_processed.csv")
    dataset.drop(columns=["date"], inplace=True)
    return dataset


def scale_data(scaler: MinMaxScaler, train_data: pd.DataFrame, test_data: pd.DataFrame) \
        -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)
    return train_data, test_data


def prepare_model_data(dataset: pd.DataFrame, scaler: MinMaxScaler):
    target_col = "available_bike_stands"
    features = list(dataset.columns)

    train_data, test_data = create_test_train_split(dataset)
    train_data, test_data = scale_data(scaler, train_data, test_data)

    target_col_idx = dataset.columns.get_loc(target_col)
    feature_cols_idx = [dataset.columns.get_loc(col) for col in features]

    X_train, y_train = create_time_series(train_data, WINDOW_SIZE, target_col_idx, feature_cols_idx)
    X_test, y_test = create_time_series(test_data, WINDOW_SIZE, target_col_idx, feature_cols_idx)

    return X_train, y_train, X_test, y_test


def evaluate_model_performance(y_true, y_pred, dataset, scaler):
    y_true_copy = np.repeat(y_true, dataset.shape[1], axis=-1)
    y_true = scaler.inverse_transform(np.reshape(y_true_copy, (len(y_true), dataset.shape[1])))[:, 0]

    prediction_copy = np.repeat(y_pred, dataset.shape[1], axis=-1)
    prediction = scaler.inverse_transform(np.reshape(prediction_copy, (len(y_pred), dataset.shape[1])))[:, 0]

    mse = mean_squared_error(y_true, prediction)
    mae = mean_absolute_error(y_true, prediction)
    evs = explained_variance_score(y_true, prediction)

    return mse, mae, evs


def write_metrics_to_file(file_path: str, model_name: str, mse: float, mae: float, evs: float) -> None:
    with open(file_path, "w") as file:
        file.write(f"Model: {model_name}\n")
        file.write(f"MSE: {mse}\n")
        file.write(f"MAE: {mae}\n")
        file.write(f"EVS: {evs}\n")
