import dropbox


from abc import abstractmethod
from typing import Protocol
from pathlib import Path

from dropbox.exceptions import ApiError


class UploadError(Exception):
    pass


class SupportUploadToCloud(Protocol):
    @abstractmethod
    def upload(self, file_path: Path):
        """Upload file to cloud storage

        :param file_path: path to file
        """
        raise NotImplementedError


class DropboxClient(SupportUploadToCloud):
    def __init__(self, app_key: str, refresh_token: str):
        self.app_key = app_key
        self.refresh_token = refresh_token

    def upload(self, file_path: Path):
        """Upload file to Dropbox

        :param file_path: path to archive
        """

        try:
            with dropbox.Dropbox(oauth2_refresh_token=self.refresh_token, app_key=self.app_key) as dbx:
                with open(file_path, "rb") as fp:
                    dbx.files_upload(fp.read(), f"/test_dropbox/{file_path.name}")
        except ApiError:
            raise UploadError('Failed to upload file to dropbox')

