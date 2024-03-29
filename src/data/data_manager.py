import os
import pandas as pd
from typing import List, Union
from pydantic import BaseModel


class DataManager:

    def __init__(self, data_path: str):
        self.data_path = data_path

    def save(self, folder: str, file_name: str, df: pd.DataFrame,
             override: bool = False) -> None:
        file_path = f"{self.data_path}/{folder}/{file_name}.csv"

        if os.path.exists(file_path) and not override:
            existing_df = pd.read_csv(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_csv(file_path, index=False)

    def get_dataframe(self, folder: str, file_name: str) -> pd.DataFrame:
        file_path = f"{self.data_path}/{folder}/{file_name}.csv"
        return pd.read_csv(file_path)

    @staticmethod
    def create_dataframe(data: Union[List[BaseModel], BaseModel]) -> pd.DataFrame:
        if isinstance(data, BaseModel):
            data = [data]

        new_rows = [row.dict() for row in data]
        return pd.DataFrame(new_rows)
