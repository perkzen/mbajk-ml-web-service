import numpy as np
import pandas as pd
import tf_keras
import tensorflow_model_optimization as tfmot
from typing import Tuple, Callable
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
from sklearn.preprocessing import MinMaxScaler
from tensorflow_model_optimization.python.core.quantization.keras.default_8bit import default_8bit_quantize_scheme
from src.config import settings
from src.models import create_time_series


def build_model(input_shape: tuple[int, int]) -> tf_keras.Sequential:
    quantize_annotate_layer = tfmot.quantization.keras.quantize_annotate_layer

    model = tf_keras.Sequential(name="GRU")

    model.add(tf_keras.Input(shape=input_shape))
    model.add(tf_keras.layers.GRU(units=128, return_sequences=True))
    model.add(tf_keras.layers.Dropout(0.2))

    model.add(tf_keras.layers.GRU(units=64, return_sequences=True))
    model.add(tf_keras.layers.Dropout(0.2))

    model.add(tf_keras.layers.GRU(units=32))

    model.add(quantize_annotate_layer(tf_keras.layers.Dense(units=32, activation="relu")))
    model.add(quantize_annotate_layer(tf_keras.layers.Dense(units=1)))

    optimizer = tf_keras.optimizers.legacy.Adam(learning_rate=0.01)

    model.compile(optimizer=optimizer, loss="mean_squared_logarithmic_error")

    tfmot.quantization.keras.quantize_apply(
        model,
        scheme=default_8bit_quantize_scheme.Default8BitQuantizeScheme(),
        quantized_layer_name_prefix='quant_'
    )

    return model


def train_model(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray,
                build_model_fn: Callable[[Tuple[int, int]], tf_keras.Sequential], epochs: int = 10, batch_size=64,
                verbose: int = 1) -> tf_keras.Sequential:
    model = build_model_fn((x_train.shape[1], x_train.shape[2]))
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test), verbose=verbose)

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
