import os
import dagshub.auth
from dagshub.data_engine.datasources import mlflow
from mlflow import MlflowClient
from src.config import settings
from src.models import get_test_train_data
from src.models.helpers import write_metrics_to_file, load_bike_station_dataset
from src.models.model import prepare_model_data, evaluate_model_performance
from src.models.model_registry import get_production_model, get_production_scaler, get_latest_model_version, \
    get_latest_scaler_version
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
    mlflow.start_run(run_name=f"mbajk_station_{station_number}", experiment_id="1")

    dataset = load_bike_station_dataset(str(station_number), "test")

    production_model = get_production_model(station_number)
    production_scaler = get_production_scaler(station_number)

    model = get_latest_model_version(station_number)
    scaler = get_latest_scaler_version(station_number)

    train_data, test_data = get_test_train_data(str(station_number))

    _, _, X_test, y_test = prepare_model_data(dataset=dataset, scaler=scaler, train_data=train_data,
                                              test_data=test_data)

    # latest model metrics
    mse_test, mae_test, evs_test = evaluate_model_performance(y_test, model.predict(X_test), dataset, scaler)

    mlflow.log_metric("MSE_test", mse_test)
    mlflow.log_metric("MAE_test", mae_test)
    mlflow.log_metric("EVS_test", evs_test)

    if production_model is None or production_scaler is None:
        # If there is no production model, set the latest model as production
        update_production_model(station_number)
    else:
        # production metrics
        mse_production, mae_production, evs_production = evaluate_model_performance(y_test,
                                                                                    production_model.predict(X_test),
                                                                                    dataset, production_scaler)

        # set model to production if it performs better
        if mse_test < mse_production:
            update_production_model(station_number)

    write_metrics_to_file(f"reports/{station_number}/metrics.txt", model.name, mse_test, mae_test, evs_test)

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
        predict_model_pipeline(station_number)


if __name__ == "__main__":
    main()
