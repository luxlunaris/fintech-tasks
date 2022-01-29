import logging
import pathlib

import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / "config" / "db.yaml"


log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
f = logging.Formatter(
    "[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)
log.addHandler(ch)


def get_config(path):
    with open(path) as f:
        config = yaml.load(f, Loader=yaml.CLoader)
    return config


config = get_config(config_path)
