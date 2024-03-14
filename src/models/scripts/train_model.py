import joblib
from sklearn.preprocessing import MinMaxScaler
from src.models.helpers import load_dataset
from src.models.model import train_model
from src.utils.decorators import execution_timer


@execution_timer("Train Model")
def main() -> None:
    dataset = load_dataset()
    scaler = MinMaxScaler()
    model = train_model(dataset, scaler)

    joblib.dump(scaler, "models/minmax_scaler.gz")
    model.save(f"models/mbajk_{model.name}_model.keras")


if __name__ == "__main__":
    main()
