import os
from sklearn.preprocessing import MinMaxScaler
from src.models.helpers import load_bike_station_dataset
from src.models.model import train_model, build_model, save_model
from src.utils.decorators import execution_timer
from multiprocessing import Pool


def train_model_in_parallel(station_number: int) -> None:
    dataset = load_bike_station_dataset(f"mbajk_station_{station_number}.csv")
    scaler = MinMaxScaler()
    model = train_model(dataset=dataset, scaler=scaler, build_model_fn=build_model, epochs=100, batch_size=7, verbose=0)

    save_model(model, scaler, station_number, "model", "minmax")
    print(f"[Train Model] - Model for station {station_number} has been trained and saved")


@execution_timer("Train Model")
def main() -> None:
    dir_path = "data/processed"
    station_numbers = [int((file.split('_')[2]).split('.')[0]) for file in os.listdir(dir_path) if
                       file.startswith('mbajk_station')]

    with Pool(processes=os.cpu_count()) as pool:
        pool.map(train_model_in_parallel, station_numbers)


if __name__ == "__main__":
    main()
