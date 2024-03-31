import os
import pandas as pd
from typing import List, Union
from pydantic import BaseModel
from dagshub import get_repo_bucket_client
from src.config import settings


class DataManager:

    def __init__(self, data_path: str):
        self.data_path = data_path

    def save(self, folder: str, file_name: str, df: pd.DataFrame,
             override: bool = False) -> None:
        file_path = f"{self.data_path}/{folder}/{file_name}.csv"

        s3 = get_repo_bucket_client(settings.repo_name)

        s3.download_file(
            Bucket=settings.bucket_name,
            Key=file_path,
            Filename=file_path,
        )

        if os.path.exists(file_path) and not override:
            existing_df = pd.read_csv(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_csv(file_path, index=False)

        s3.upload_file(
            Bucket=settings.bucket_name,
            Filename=file_path,
            Key=file_path,
        )

    def get_dataframe(self, folder: str, file_name: str) -> pd.DataFrame:
        file_path = f"{self.data_path}/{folder}/{file_name}.csv"
        return pd.read_csv(file_path)

    @staticmethod
    def create_dataframe(data: Union[List[BaseModel], BaseModel]) -> pd.DataFrame:
        if isinstance(data, BaseModel):
            data = [data]

        new_rows = [row.dict() for row in data]
        return pd.DataFrame(new_rows)

    @staticmethod
    def get_s3_client():
        return get_repo_bucket_client(settings.repo_name)