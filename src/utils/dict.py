from typing import List


def add_keys_to_dict(data: dict, keys: List[str]) -> dict:
    new_data = {}
    for key in keys:
        new_data[key] = data[key]
    return new_data
