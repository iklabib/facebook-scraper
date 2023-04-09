from ruamel.yaml import YAML
from pathlib import Path
from typing import Union

_yaml = YAML(typ='safe')
CONFIG_PATH = Path(__file__).parent / 'config.yaml'


def open_config(file_path: Union[Path, str]) -> dict:
    with open(file_path) as r:
        return _yaml.load(r.read())


def load() -> dict:
    return open_config(CONFIG_PATH)
