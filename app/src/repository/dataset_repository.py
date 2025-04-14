"""
Содержит репозитории приложения.
Репозиторий напрямую работает с БД - добавляет, изменяет, удаляет и ищет записи в БД.
"""
import json
import os
from typing import Optional

from bson import ObjectId
from flask import current_app, g
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy

from app.src.models.Dataset import Dataset
from app.src.models.DatasetBrief import DatasetBrief


def get_db():
    """
    Геттер экземпляра БД
    """
    db_name = os.getenv('DB_NAME')

    dbase = getattr(g, db_name, None)

    if dbase is None:
        dbase = g._database = PyMongo(current_app).cx[db_name]

    return dbase


db = LocalProxy(get_db)


class DatasetRepository:
    """
    Класс-репозиторий для данных, связанных с датасетами.
    """

    @staticmethod
    def get_all_datasets_brief() -> list:
        """
        Возвращает список Brief'ов всех датасетов в БД. Если БД пустая, то возвращается пустой список.
        """
        briefs = [
            DatasetBrief(
                "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
                "name",
                "description",
                "CSV",
                1
            )
        ]

        return briefs

    @staticmethod
    def add_dataset(dataset: Dataset) -> None:
        """
        Добавляет датасет в БД.
        """
        db['DatasetCollection'].insert_one(dataset.to_dict())

    @staticmethod
    def edit_dataset(dataset: Dataset) -> None:
        """
        Изменяет датасет в БД.
        """
        db['DatasetCollection'].update_one(dataset.to_dict())
