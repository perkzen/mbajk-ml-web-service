import os


def write_metrics_to_file(file_path: str, model_name: str, mse: float, mae: float, evs: float) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
        file.write(f"Model: {model_name}\n")
        file.write(f"MSE: {mse}\n")
        file.write(f"MAE: {mae}\n")
        file.write(f"EVS: {evs}\n")
