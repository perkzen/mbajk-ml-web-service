import joblib
import numpy as np
import pandas as pd
from test_train_split import create_test_train_split
from time_series import create_time_series
from keras.models import load_model
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score


def evaluate_model_performance(y_true, y_pred, dataset, scaler):
    y_true_copy = np.repeat(y_true, dataset.shape[1], axis=-1)
    y_true = scaler.inverse_transform(np.reshape(y_true_copy, (len(y_true), dataset.shape[1])))[:, 0]

    prediction_copy = np.repeat(y_pred, dataset.shape[1], axis=-1)
    prediction = scaler.inverse_transform(np.reshape(prediction_copy, (len(y_pred), dataset.shape[1])))[:, 0]

    mse = mean_squared_error(y_true, prediction)
    mae = mean_absolute_error(y_true, prediction)
    evs = explained_variance_score(y_true, prediction)

    return mse, mae, evs


if __name__ == "__main__":
    model = load_model("models/mbajk_GRU_model.keras")
    scaler = joblib.load("models/minmax_scaler.gz")

    dataset = pd.read_csv("data/processed/mbajk_processed.csv")
    dataset.drop(columns=["date"], inplace=True)

    target_col = "available_bike_stands"
    features = [target_col] + [col for col in dataset.columns if col != target_col]

    dataset = dataset[features]

    train_data, test_data = create_test_train_split(dataset)
    window_size = 50

    target_col_idx = dataset.columns.get_loc(target_col)
    feature_cols_idx = [dataset.columns.get_loc(col) for col in features]

    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)

    X_train, y_train = create_time_series(train_data, window_size, target_col_idx, feature_cols_idx)
    X_test, y_test = create_time_series(test_data, window_size, target_col_idx, feature_cols_idx)

    mse_train, mae_train, evs_train = evaluate_model_performance(y_train, model.predict(X_train), dataset, scaler)
    mse_test, mae_test, evs_test = evaluate_model_performance(y_test, model.predict(X_test), dataset, scaler)

    with open("reports/train_metrics.txt", "w") as file:
        file.write(f"Model: {model.name}\n")
        file.write(f"Train MSE: {mse_train}\n")
        file.write(f"Train MAE: {mae_train}\n")
        file.write(f"Train EVS: {evs_train}\n")

    with open("reports/metrics.txt", "w") as file:
        file.write(f"Model: {model.name}\n")
        file.write(f"Test MSE: {mse_test}\n")
        file.write(f"Test MAE: {mae_test}\n")
        file.write(f"Test EVS: {evs_test}\n")
