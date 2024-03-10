import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
from sklearn.preprocessing import MinMaxScaler
from time_series import create_time_series
from model import build_model
from test_train_split import create_test_train_split

if __name__ == "__main__":
    dataset = pd.read_csv("data/processed/mbajk_processed.csv")
    dataset.drop(columns=["date"], inplace=True)

    target_col = "available_bike_stands"
    features = [target_col] + [col for col in dataset.columns if col != target_col]
    dataset = dataset[features]

    train_data, test_data = create_test_train_split(dataset)

    scaler = MinMaxScaler()
    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)

    window_size = 50

    target_col_idx = dataset.columns.get_loc(target_col)
    feature_cols_idx = [dataset.columns.get_loc(col) for col in features]

    X_train, y_train = create_time_series(train_data, window_size, target_col_idx, feature_cols_idx)
    X_test, y_test = create_time_series(test_data, window_size, target_col_idx, feature_cols_idx)

    model = build_model(input_shape=(X_train.shape[1], X_train.shape[2]))
    model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test), verbose=1)

    joblib.dump(scaler, "models/minmax_scaler.gz")
    model.save(f"models/mbajk_{model.name}_model.keras")
