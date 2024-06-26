import joblib
import numpy as np
import pandas as pd
import onnxruntime as ort
from typing import Any, List
from sklearn.preprocessing import MinMaxScaler
from ..dto import PredictionDTO
from ...config import settings
from ...data.data_fetcher import DataFetcher
from ...utils.dict import add_keys_to_dict


class MLService:
    def __init__(self, model_name: str, scaler_name: str):
        self.model = ort.InferenceSession(f"models/{model_name}_production.onnx")
        self.scaler: MinMaxScaler = joblib.load(f"models/{scaler_name}_scaler_production.gz")

    def predict(self, data: List[dict]) -> int:
        prepared_data = self.__prepare_data(data)

        predicted = self.model.run(["output"], {"input": prepared_data})[0]

        prediction_copies = np.repeat(predicted, prepared_data.shape[2], axis=-1)
        predicted = self.scaler.inverse_transform(
            np.reshape(prediction_copies, (len(predicted), prepared_data.shape[2])))[:, 0]

        return predicted[0]

    def predict_multiple(self, data: List[dict], n_future: int) -> List[PredictionDTO]:
        data_fetcher = DataFetcher(lat=settings.lat, lon=settings.lon)
        res = data_fetcher.get_weather_forecast_for_next_n_hours(hours=n_future)

        required_keys = list(data[0].keys())
        required_keys.remove("available_bike_stands")

        predictions: List[PredictionDTO] = []

        for n in range(n_future):
            prediction = max(0, int(self.predict(data)))

            predictions.append(PredictionDTO(prediction=prediction, date=f"{res[n].date}:00"))

            new_data = add_keys_to_dict(res[n].model_dump(), required_keys)
            new_data["available_bike_stands"] = prediction

            data.append(new_data)
            data.pop(0)

        return predictions

    def __prepare_data(self, data: List[dict]) -> np.ndarray[Any, np.dtype]:
        data = [item for item in data]
        data_values = []
        for item in data:
            values = list(item.values())
            data_values.append(values)

        data_keys = list(data[0].keys())
        data = pd.DataFrame(data_values, columns=data_keys)

        scaled_data = self.scaler.transform(data)

        return self.__create_time_series(scaled_data, settings.window_size, list(range(0, len(data_values[0]))))

    @staticmethod
    def __create_time_series(data, window_size, feature_cols) -> np.ndarray[Any, np.dtype]:
        sequences = []
        n_samples = len(data)

        for i in range(window_size, n_samples + 1):
            sequence = data[i - window_size:i, feature_cols]
            sequences.append(sequence)

        return np.array(sequences)
