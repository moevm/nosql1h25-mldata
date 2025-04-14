"""
Создает сущность Flask и запускает ее. Добавляет к ней пути с помощью blueprint.
"""

import os
from urllib.parse import quote_plus

from flask import Flask

from src.routers import dataset_routes

if __name__ == '__main__':
    app: Flask = Flask(__name__)
    app.register_blueprint(dataset_routes.bp)

    user = os.getenv("USR")
    password = os.getenv("PWD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")

    app.config['MONGO_URI'] = f"mongodb://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}"
    app.config['UPLOAD_FOLDER'] = os.getenv('DATASET_DIR', './datasets')

    app.run()
