from typing import List

import pandas as pd

from src.config import settings
from src.serve.dto import PredictBikesDTO


class DataService:

    def __init__(self):
        self.dataset = pd.read_csv("data/processed/mbajk_processed.csv")

    def get_latest_data(self) -> List[PredictBikesDTO]:
        data = self.dataset.tail(settings.window_size).to_dict(orient="records")
        return [PredictBikesDTO.from_dataset(item) for item in data]
