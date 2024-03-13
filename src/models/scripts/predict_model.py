import joblib
from keras.models import load_model
from src.models.helpers import evaluate_model_performance, prepare_model_data, write_metrics_to_file, load_dataset
from src.utils.decorators import execution_timer


@execution_timer("Predict Model")
def main() -> None:
    dataset = load_dataset()
    model = load_model("models/mbajk_GRU_model.keras")
    scaler = joblib.load("models/minmax_scaler.gz")

    X_train, y_train, X_test, y_test, _ = prepare_model_data(dataset=dataset, scaler=scaler)

    mse_train, mae_train, evs_train = evaluate_model_performance(y_train, model.predict(X_train), dataset, scaler)
    mse_test, mae_test, evs_test = evaluate_model_performance(y_test, model.predict(X_test), dataset, scaler)

    write_metrics_to_file("reports/train_metrics.txt", model.name, mse_train, mae_train, evs_train)
    write_metrics_to_file("reports/metrics.txt", model.name, mse_test, mae_test, evs_test)


if __name__ == "__main__":
    main()
