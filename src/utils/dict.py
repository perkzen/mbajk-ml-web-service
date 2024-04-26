from typing import List


def add_keys_to_dict(data: dict, keys: List[str], skip_keys: List[str] = None) -> dict:
    if skip_keys is None:
        skip_keys = []

    new_data = {}
    for key in keys:
        if key in skip_keys:
            continue
        new_data[key] = data[key]
    return new_data
