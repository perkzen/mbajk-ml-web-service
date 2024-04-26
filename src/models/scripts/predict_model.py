import os
import dagshub.auth
import onnxruntime as ort
from dagshub.data_engine.datasources import mlflow
from mlflow import MlflowClient
from src.config import settings
from src.models import get_test_train_data
from src.models.helpers import write_metrics_to_file, load_bike_station_dataset
from src.models.model import prepare_model_data, evaluate_model_performance
from src.models.model_registry import download_model, ModelType
from src.utils.decorators import execution_timer


def update_production_model(station_number: int) -> None:
    client = MlflowClient()

    new_model_version = client.get_latest_versions("mbajk_station_" + str(station_number), stages=["staging"])[
        0].version
    new_scaler_version = \
        client.get_latest_versions("mbajk_station_" + str(station_number) + "_scaler", stages=["staging"])[0].version

    client.transition_model_version_stage("mbajk_station_" + str(station_number), new_model_version, "production")
    client.transition_model_version_stage("mbajk_station_" + str(station_number) + "_scaler", new_scaler_version,
                                          "production")
    print(f"[Update Model] - New model for station {station_number} has been set to production")


def predict_model_pipeline(station_number: int) -> None:
    mlflow.start_run(run_name=f"mbajk_station_{station_number}", experiment_id="1", nested=True)

    dataset = load_bike_station_dataset(str(station_number), "test")

    production_model_path, production_scaler = download_model(station_number, ModelType.PRODUCTION)
    latest_model_path, scaler = download_model(station_number, ModelType.LATEST)

    if latest_model_path is None and scaler is None:
        # we don't have a staging model because previous staging model was set to production
        # this could happen when running locally
        return

    if production_model_path is None and production_scaler is None:
        update_production_model(station_number)
        return

    latest_model = ort.InferenceSession(latest_model_path)
    production_model = ort.InferenceSession(production_model_path)

    train_data, test_data = get_test_train_data(str(station_number))

    _, _, X_test, y_test = prepare_model_data(dataset=dataset, scaler=scaler, train_data=train_data,
                                              test_data=test_data)

    latest_model_predictions = latest_model.run(["output"], {"input": X_test})[0]
    mse_test, mae_test, evs_test = evaluate_model_performance(y_test, latest_model_predictions, dataset, scaler)

    mlflow.log_metric("MSE_test", mse_test)
    mlflow.log_metric("MAE_test", mae_test)
    mlflow.log_metric("EVS_test", evs_test)

    production_model_predictions = production_model.run(["output"], {"input": X_test})[0]
    mse_production, mae_production, evs_production = evaluate_model_performance(y_test,
                                                                                production_model_predictions,
                                                                                dataset, production_scaler)
    # set model to production if it performs better
    if mse_test < mse_production:
        update_production_model(station_number)

    write_metrics_to_file(f"reports/{station_number}/metrics.txt", "GRU", mse_test, mae_test, evs_test)

    print(f"[Predict Model] - Train metrics for station {station_number} have been calculated")

    mlflow.end_run()


@execution_timer("Predict Model")
def main() -> None:
    dir_path = "data/processed"
    station_numbers = [int(folder) for folder in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, folder))]

    dagshub.auth.add_app_token(token=settings.dagshub_user_token)
    dagshub.init("mbajk-ml-web-service", "perkzen", mlflow=True)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    for station_number in station_numbers:
        print(f"[Predict Model] - Predicting model for station {station_number}")
        predict_model_pipeline(station_number)


if __name__ == "__main__":
    main()
