import yaml
from os.path import realpath, join

from pathlib import Path


def config_decorator(class_):
    base_path = Path(realpath(join(__file__, '..')))
    class_.BASE_PATH = base_path
    class_.TMP_PATH = base_path / 'tmp'

    with open(class_.BASE_PATH / f"config.yaml", "r") as fp:
        yaml_config = yaml.load(fp, Loader=yaml.CBaseLoader)

    class_.USERNAME = yaml_config['username']
    class_.PASSWORD = yaml_config['password']

    class_.CLOUD_STORAGES = yaml_config['storages']

    return class_


@config_decorator
class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"
    SECRET_KEY = "changeme"
    HOST = "0.0.0.0"
    PORT = "5000"


class TestingConfig(DevelopmentConfig):
    TESTING = True


class ProductionConfig(Config):
    pass
