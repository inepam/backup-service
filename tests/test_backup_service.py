import sys
import pytest
import shutil
import base64

sys.path.insert(0, "backup_service")

TEST_DIRECTORY: str = "test_directory"
TEST_FILE_NAME: str = "test_file"

from backup_service import __version__
from app import create_app
from config import Config
from core.backuper import Backuper
from core.clients import MockClient


def test_version():
    assert __version__ == '0.1.0'


def test_creates_app_successfully():
    app = create_app(Backuper(), "config.TestingConfig")
    assert app is not None


@pytest.fixture
def app():
    backuper = Backuper()
    backuper.clients = {'mock_client': MockClient()}
    app = create_app(backuper, "config.TestingConfig")
    yield app


@pytest.fixture
def directory_to_archive():
    path = Config.TMP_PATH / TEST_DIRECTORY
    dir_exists = path.exists() and path.is_dir()
    if not dir_exists:
        path.mkdir(parents=True)
    file_path = path / TEST_FILE_NAME
    with open(file_path, 'w') as f:
        f.writelines("archiver test file")
    yield path
    if dir_exists:
        file_path.unlink()
    else:
        shutil.rmtree(path)


def test_returns_403_when_no_credentials(app):
    with app.test_client() as client:
        response = client.post('/api/backup', data=dict(path="/tmp/some_dir"))
        assert response.status_code == 403


def test_returns_403_when_invalid_credentials(app):
    invalid_credentials = base64.b64encode(b"testuser:testpassword").decode("utf-8")
    with app.test_client() as client:
        response = client.post('/api/backup',
                               headers={"Authorization": "Basic " + invalid_credentials},
                               data={"path": "/tmp/some_dir"})
        assert response.status_code == 403


def test_returns_400_when_no_path_provided(app):
    valid_credentials = base64.b64encode(b"johndoe:password").decode("utf-8")
    with app.test_client() as client:
        response = client.post('/api/backup',
                               headers={"Authorization": "Basic " + valid_credentials})
        assert response.status_code == 400


def test_successfully_uploads_file(app, directory_to_archive):
    valid_credentials = base64.b64encode(b"johndoe:password").decode("utf-8")
    with app.test_client() as client:
        response = client.post('/api/backup',
                               headers={"Authorization": "Basic " + valid_credentials},
                               data={"path": str(directory_to_archive)})
        assert response.status_code == 200
