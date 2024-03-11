import joblib
from typing import Any, List
import numpy as np
import pandas as pd
from keras import Model
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from ..dto.bike_station_dto import BikeStationDto
from ...config import WINDOW_SIZE


class MLService:
    def __init__(self, model_name: str, scaler_name: str):
        self.model: Model = load_model(f"models/{model_name}.keras")
        self.scaler: MinMaxScaler = joblib.load(f"models/{scaler_name}_scaler.gz")

    def predict(self, data: List[BikeStationDto]) -> int:
        prepared_data = self.__prepare_data(data)

        predicted = self.model.predict(prepared_data)

        prediction_copies = np.repeat(predicted, prepared_data.shape[2], axis=-1)
        predicted = self.scaler.inverse_transform(
            np.reshape(prediction_copies, (len(predicted), prepared_data.shape[2])))[:, 0]

        return predicted[0]

    def __prepare_data(self, data: List[BikeStationDto]) -> np.ndarray[Any, np.dtype]:
        data = [item.model_dump() for item in data]
        data_values = []
        for item in data:
            values = list(item.values())
            data_values.append(values)

        data_keys = list(data[0].keys())
        data = pd.DataFrame(data_values, columns=data_keys)

        scaled_data = self.scaler.transform(data)

        return self.__create_time_series(scaled_data, WINDOW_SIZE, list(range(0, len(data_values[0]))))

    @staticmethod
    def __create_time_series(data, window_size, feature_cols) -> np.ndarray[Any, np.dtype]:
        sequences = []
        n_samples = len(data)

        for i in range(window_size, n_samples + 1):
            sequence = data[i - window_size:i, feature_cols]
            sequences.append(sequence)

        return np.array(sequences)
