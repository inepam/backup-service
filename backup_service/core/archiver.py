import tarfile

from pathlib import Path
from time import time

from config import Config


def create_archive(source_path: str) -> Path:
    """Create tar archive of selected directory

    :param source_path: path to selected directory
    :return: path to archive file
    """
    output = Config.TMP_PATH / f"backup-{int(time())}.tar.gz"
    path = Path(source_path)
    if path.exists() and path.is_dir():
        with tarfile.open(output, "w:gz") as tar:
            tar.add(path, arcname=".")
    else:
        raise FileNotFoundError("Selected directory does not exist")
    return output
