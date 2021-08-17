import json
from pathlib import Path
from typing import Dict

BASE_PATH = Path.cwd().joinpath('..', 'tests', 'data')


def read_file(file_name: str) -> Dict[str, str]:
    path = get_file_with_json_extension(file_name)

    with path.open(mode='r') as f:
        return json.load(f)


def get_file_with_json_extension(file_name: str) -> str:
    if '.json' in file_name:
        path = BASE_PATH.joinpath(file_name)
    else:
        path = BASE_PATH.joinpath(f'{file_name}.json')
    return path
