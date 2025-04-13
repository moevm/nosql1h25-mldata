"""
Создает сущность Flask и запускает ее. Добавляет к ней пути с помощью blueprint.
"""

from flask import Flask

from app.src.routers import dataset_routes

if __name__ == '__main__':
    app: Flask = Flask(__name__)
    app.register_blueprint(dataset_routes.bp)

    print('http://127.0.0.1:5000/datasets')

    app.run()
