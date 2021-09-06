from core.clients import DropboxClient, SupportUploadToCloud, UploadError
from config import Config
from core.archiver import create_archive


class BackupError(Exception):
    pass


class Backuper:
    def __init__(self):
        self.clients: dict[str, SupportUploadToCloud] = {
            'dropbox': DropboxClient(app_key=Config.CLOUD_STORAGES['dropbox']['app_key'],
                                     refresh_token=Config.CLOUD_STORAGES['dropbox']['refresh_token'])
        }

    def backup_directory(self, directory_path: str):
        try:
            archive_path = create_archive(directory_path)
        except FileNotFoundError:
            raise BackupError('Failed to create archive')

        try:
            for _, client in self.clients.items():
                client.upload(archive_path)
        except UploadError:
            raise BackupError('Failed to upload file to dropbox')

        archive_path.unlink(missing_ok=True)
