import sys

sys.path.insert(0, "backup_service")

from backup_service import __version__
from backup_service.app import create_app


def test_version():
    assert __version__ == '0.1.0'


def test_creates_app_successfully():
    app = create_app("config.TestingConfig")
    assert app is not None
