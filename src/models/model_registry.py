import os

import dagshub
import dagshub.auth as dh_auth
from mlflow.keras import load_model as mlflow_load_model
from mlflow.sklearn import load_model as load_scaler
from dagshub.data_engine.datasources import mlflow
from mlflow import MlflowClient
from src.config import settings

from src.models.model import save_model


def get_latest_model_version(station_number: int):
    client = MlflowClient()
    model_version = client.get_latest_versions("mbajk_station_" + str(station_number), stages=["staging"])[0]
    model_url = model_version.source
    model = mlflow_load_model(model_url)
    return model


def get_latest_scaler_version(station_number: int):
    client = MlflowClient()
    model_version = \
        client.get_latest_versions("mbajk_station_" + str(station_number) + "_scaler", stages=["staging"])[0]
    model_url = model_version.source
    scaler = load_scaler(model_url)

    return scaler


def get_production_model(station_number: int):
    try:
        client = MlflowClient()
        model_version = client.get_latest_versions("mbajk_station_" + str(station_number), stages=["production"])[0]
        model_url = model_version.source
        production_model = mlflow_load_model(model_url)
        return production_model
    except IndexError:
        print(f"Production model for station {station_number} not found.")
        return None


def get_production_scaler(station_number: int):
    try:
        client = MlflowClient()
        model_version = \
            client.get_latest_versions("mbajk_station_" + str(station_number) + "_scaler", stages=["production"])[0]
        model_url = model_version.source
        production_scaler = load_scaler(model_url)
        return production_scaler
    except IndexError:
        print(f"Production scaler for station {station_number} not found.")
        return None


def download_model_registry():
    dh_auth.add_app_token(token=settings.dagshub_user_token)
    dagshub.init("mbajk-ml-web-service", "perkzen", mlflow=True)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    dir_path = "models"
    station_numbers = [int(folder) for folder in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, folder))]

    for i in station_numbers:
        # # skip if model already exists
        if os.path.exists(f"models/{i}"):
            print(f"Model for station {i} already exists.")
            continue

        model = get_production_model(i)
        scaler = get_production_scaler(i)

        save_model(model, scaler, i, "model", "minmax")
        print(f"Model for station {i} has been downloaded.")
