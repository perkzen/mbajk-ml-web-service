from typing import List

import pandas as pd


def add_keys_to_dict(data: dict, keys: List[str], skip_keys: List[str] = None) -> dict:
    if skip_keys is None:
        skip_keys = []

    new_data = {}
    for key in keys:
        if key in skip_keys:
            continue
        new_data[key] = data[key]
    return new_data


def add_custom_keys_to_dict(data: dict, keys: List[str], date: str) -> dict:
    date_time = pd.to_datetime(date)

    for key in keys:
        if key == "weekend":
            data[key] = 1 if date_time.weekday() in [5, 6] else 0
        elif key == "is_day":
            data[key] = 1 if 6 <= date_time.hour <= 18 else 0
        elif key == "season":
            data[key] = (date_time.month % 12 + 3) // 3
        elif key == "hour":
            data[key] = date_time.hour
        elif key == "day_of_week":
            data[key] = date_time.weekday()

    return data
