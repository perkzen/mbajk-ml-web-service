import os
import joblib
import numpy as np
import pandas as pd
from typing import Tuple, Callable
from keras import Sequential
from keras.layers import Dense, GRU, Dropout, Input
from keras.optimizers import Adam
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
from sklearn.preprocessing import MinMaxScaler
from src.config import settings
from src.models import create_time_series


def build_model(input_shape: tuple[int, int]) -> Sequential:
    model = Sequential(name="GRU")

    model.add(Input(shape=input_shape))
    model.add(GRU(units=128, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(GRU(units=64, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(GRU(units=32))

    model.add(Dense(units=32, activation="relu"))
    model.add(Dense(units=1))

    optimizer = Adam(learning_rate=0.01)
    model.compile(optimizer=optimizer, loss="mean_squared_logarithmic_error")

    return model


def train_model(dataset: pd.DataFrame, scaler: MinMaxScaler, test_dataset: pd.DataFrame, train_dataset: pd.DataFrame,
                build_model_fn: Callable[[Tuple[int, int]], Sequential], epochs: int = 10, batch_size=64,
                verbose: int = 1) -> Sequential:
    X_train, y_train, X_test, y_test = prepare_model_data(dataset=dataset, scaler=scaler, train_data=train_dataset,
                                                          test_data=test_dataset)

    model = build_model_fn((X_train.shape[1], X_train.shape[2]))
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=verbose)

    return model


def evaluate_model_performance(y_true, y_pred, dataset, scaler):
    y_true_copy = np.repeat(y_true, dataset.shape[1], axis=-1)
    y_true = scaler.inverse_transform(np.reshape(y_true_copy, (len(y_true), dataset.shape[1])))[:, 0]

    prediction_copy = np.repeat(y_pred, dataset.shape[1], axis=-1)
    prediction = scaler.inverse_transform(np.reshape(prediction_copy, (len(y_pred), dataset.shape[1])))[:, 0]

    mse = mean_squared_error(y_true, prediction)
    mae = mean_absolute_error(y_true, prediction)
    evs = explained_variance_score(y_true, prediction)

    return mse, mae, evs


def save_model(model: Sequential, scaler: MinMaxScaler, station_number: int, model_name: str, scaler_name: str) -> None:
    folder_name = f"models/station_{station_number}"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    joblib.dump(scaler, f"{folder_name}/{scaler_name}_scaler.gz")
    model.save(f"{folder_name}/{model_name}.keras")


def prepare_model_data(dataset: pd.DataFrame, scaler: MinMaxScaler, train_data: pd.DataFrame,
                       test_data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    target_col = "available_bike_stands"
    features = list(dataset.columns)

    train_data, test_data = scale_data(scaler, train_data, test_data)

    target_col_idx = dataset.columns.get_loc(target_col)
    feature_cols_idx = [dataset.columns.get_loc(col) for col in features]

    X_train, y_train = create_time_series(train_data, settings.window_size, target_col_idx, feature_cols_idx)
    X_test, y_test = create_time_series(test_data, settings.window_size, target_col_idx, feature_cols_idx)

    return X_train, y_train, X_test, y_test


def scale_data(scaler: MinMaxScaler, train_data: pd.DataFrame, test_data: pd.DataFrame) \
        -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)
    return train_data, test_data
