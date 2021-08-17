from json import loads
from typing import Any


def get_prop_from_str_payload(payload: str, property: str) -> Any:
    json_obj = loads(payload)
    try:
        prop_value = json_obj[property]
    except:
        print(f"Property {property} does not exist in provided payload")

    return prop_value