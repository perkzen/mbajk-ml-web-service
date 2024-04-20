import os

import dagshub
from sklearn.preprocessing import MinMaxScaler
import dagshub.auth as dh_auth

from src.config import settings
from src.models import create_test_train_split
from src.models.helpers import load_bike_station_dataset
from src.models.model import train_model, build_model, save_model
from src.utils.decorators import execution_timer
from multiprocessing import Pool
import mlflow


def train_model_in_parallel(station_number: int) -> None:
    dataset = load_bike_station_dataset(station_number)
    scaler = MinMaxScaler()

    train_data, test_data = create_test_train_split(str(station_number))

    mlflow.start_run(run_name="mbajk_station_" + str(station_number))

    model = train_model(dataset=dataset, scaler=scaler, build_model_fn=build_model, epochs=10, batch_size=32,
                        verbose=0, train_dataset=train_data, test_dataset=test_data)

    mlflow.log_param("epochs", 10)
    mlflow.log_param("batch_size", 32)
    mlflow.log_param("dataset_size", len(dataset))

    mlflow.end_run()

    save_model(model, scaler, station_number, "model", "minmax")
    print(f"[Train Model] - Model for station {station_number} has been trained and saved")


@execution_timer("Train Model")
def main() -> None:
    dir_path = "data/processed"
    station_numbers = [int(folder) for folder in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, folder))]

    dh_auth.add_app_token(token=settings.dagshub_user_token)
    dagshub.init("mbajk-ml-web-service", "perkzen", mlflow=True)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    with Pool(processes=os.cpu_count()) as pool:
        pool.map(train_model_in_parallel, station_numbers)


if __name__ == "__main__":
    main()
