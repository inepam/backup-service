import logging

from flask import Flask, request
from werkzeug.security import check_password_hash

from config import Config
from core.backuper import Backuper, BackupError


def create_app(backuper: Backuper, config_object: str = "config.ProductionConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('app')

    if not Config.TMP_PATH.exists():
        Config.TMP_PATH.mkdir()

    @app.route("/api/backup", methods=["POST"])
    def backup():
        """Create backup of selected directory"""

        path = request.form.get("path")

        if path is None:
            return "Bad request", 400

        if request.authorization:
            username = request.authorization.username
            password = request.authorization.password
            if username == Config.USERNAME and check_password_hash(Config.PASSWORD, password):
                try:
                    backuper.backup_directory(path)
                except BackupError:
                    logger.error('Upload error.', exc_info=True)
                    return "Server error", 500
                return "OK", 200
            else:
                return "Forbidden", 403
        else:
            return "Forbidden", 403

    return app


if __name__ == "__main__":
    dev_app = create_app(Backuper(), "config.DevelopmentConfig")
    dev_app.run()
