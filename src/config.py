import pathlib
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    window_size: int = 24
    top_features: int = 4
    lat: float = 46.5547
    lon: float = 15.6467
    mbajk_api_key: str
    mlflow_tracking_username: str
    mlflow_tracking_uri: str
    mlflow_tracking_password: str
    dagshub_user_token: str
    custom_dataset_columns: List[str] = ["hour", "is_day", "season", "weekend", "day_of_week"]

    __project_root = pathlib.Path(__file__).resolve().parent.parent

    model_config = SettingsConfigDict(env_file=f"{__project_root}/.env")


settings = Settings()
