import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from time_series import create_time_series
from model import build_model

if __name__ == "__main__":
    dataset = pd.read_csv("data/processed/mbajk_processed.csv")
    dataset.drop(columns=["date"], inplace=True)

    target_col = "available_bike_stands"
    features = [target_col] + [col for col in dataset.columns if col != target_col]
    dataset = dataset[features]

    test_split = round(len(dataset) * 0.2)
    train_data = dataset[:-test_split]
    test_data = dataset[-test_split:]

    scaler = MinMaxScaler()
    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)

    window_size = 25

    target_col_idx = dataset.columns.get_loc(target_col)
    feature_cols_idx = [dataset.columns.get_loc(col) for col in features]

    X_train, y_train = create_time_series(train_data, window_size, target_col_idx, feature_cols_idx)
    X_test, y_test = create_time_series(test_data, window_size, target_col_idx, feature_cols_idx)

    model = build_model(input_shape=(X_train.shape[1], X_train.shape[2]))
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=1)

    joblib.dump(scaler, "models/minmax_scaler.gz")
    model.save(f"models/mbajk_{model.name}_model.keras")
