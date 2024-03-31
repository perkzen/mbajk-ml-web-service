import pathlib
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    window_size: int = 48
    top_features: int = 4
    lat: float = 46.5547
    lon: float = 15.6467
    mbajk_api_key: str
    custom_dataset_columns: List[str] = ["hour", "is_day", "season", "weekend", "day_of_week"]
    repo_name: str = "perkzen/mbajk-ml-web-service"
    bucket_name: str = "mbajk-ml-web-service"
    dagshub_user_token: str

    __project_root = pathlib.Path(__file__).resolve().parent.parent

    model_config = SettingsConfigDict(env_file=f"{__project_root}/.env")


settings = Settings()
