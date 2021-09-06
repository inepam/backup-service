import pytest
import shutil
import sys

sys.path.insert(0, "backup_service")

from core.archiver import create_archive
from config import Config


TEST_DIRECTORY: str = "test_directory"
TEST_FILE_NAME: str = "test_file"


@pytest.fixture
def directory_to_archive():
    path = Config.TMP_PATH / TEST_DIRECTORY
    dir_exists = path.exists() and path.is_dir()
    if not dir_exists:
        path.mkdir()
    file_path = path / TEST_FILE_NAME
    with open(file_path, 'w') as f:
        f.writelines("archiver test file")
    yield
    if dir_exists:
        file_path.unlink()
    else:
        shutil.rmtree(path)


def test_creates_archive_successfully(directory_to_archive):
    archive_path = create_archive(str(Config.TMP_PATH / TEST_DIRECTORY))
    assert archive_path.exists()
    archive_path.unlink()


def test_raises_file_not_found_exception_if_dir_not_exists():
    with pytest.raises(FileNotFoundError):
        create_archive(TEST_DIRECTORY + "foo")
