import joblib
from sklearn.preprocessing import MinMaxScaler
from src.models import build_model
from src.models.helpers import prepare_model_data, load_dataset
from src.utils.decorators import execution_timer


@execution_timer("Train Model")
def main() -> None:
    scaler = MinMaxScaler()
    dataset = load_dataset()
    X_train, y_train, X_test, y_test = prepare_model_data(dataset=dataset, scaler=scaler)

    model = build_model(input_shape=(X_train.shape[1], X_train.shape[2]))
    model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test), verbose=1)

    joblib.dump(scaler, "models/minmax_scaler.gz")
    model.save(f"models/mbajk_{model.name}_model.keras")


if __name__ == "__main__":
    main()
