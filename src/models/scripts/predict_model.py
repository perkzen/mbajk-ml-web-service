import os
import joblib
from keras.models import load_model
from src.models.helpers import write_metrics_to_file, load_dataset, load_bike_station_dataset
from src.models.model import prepare_model_data, evaluate_model_performance
from src.utils.decorators import execution_timer
from multiprocessing import Pool


def predict_model_in_parallel(station_number: int) -> None:
    dataset = load_bike_station_dataset(f"mbajk_station_{station_number}.csv")
    model = load_model(f"models/station_{station_number}/model.keras")
    scaler = joblib.load(f"models/station_{station_number}/minmax_scaler.gz")

    X_train, y_train, X_test, y_test = prepare_model_data(dataset=dataset, scaler=scaler)

    mse_train, mae_train, evs_train = evaluate_model_performance(y_train, model.predict(X_train), dataset, scaler)
    mse_test, mae_test, evs_test = evaluate_model_performance(y_test, model.predict(X_test), dataset, scaler)

    write_metrics_to_file(f"reports/station_{station_number}/train_metrics.txt", model.name, mse_train, mae_train,
                          evs_train)
    write_metrics_to_file(f"reports/station_{station_number}/metrics.txt", model.name, mse_test, mae_test, evs_test)

    print(f"[Predict Model] - Train metrics for station {station_number} have been calculated")


@execution_timer("Predict Model")
def main() -> None:
    dir_path = "data/processed"
    station_numbers = [int((file.split('_')[2]).split('.')[0]) for file in os.listdir(dir_path) if
                       file.startswith('mbajk_station')]

    with Pool(processes=os.cpu_count()) as pool:
        pool.map(predict_model_in_parallel, station_numbers)


if __name__ == "__main__":
    main()
