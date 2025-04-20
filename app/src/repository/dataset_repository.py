"""
Содержит репозитории приложения.
Репозиторий напрямую работает с БД - добавляет, изменяет, удаляет и ищет записи в БД.
"""
import os
import pymongo
from typing import Optional

from typing import Any
from bson import ObjectId
from flask import current_app, g
from flask_pymongo import PyMongo
from pymongo.results import InsertOneResult
from werkzeug.local import LocalProxy

from app.src.models.Dataset import Dataset
from app.src.models.DatasetBrief import DatasetBrief


# --- Database Connection ---
uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
db = None

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB for DatasetRepository.")
    db_name = os.getenv('MONGO_DB_NAME')
    db = client[db_name]
except Exception as e:
    print(f"Error connecting to MongoDB for DatasetRepository: {e}")


def get_db():
    """
    Геттер экземпляра БД
    """
    db_name = os.getenv('MONGO_DB_NAME')

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
    def get_all_datasets_brief() -> list[DatasetBrief]:
        """
        Возвращает список Brief'ов всех датасетов в БД из коллекции DatasetInfo.
        Если БД пустая или недоступна, то возвращается пустой список.
        """
        briefs: list[DatasetBrief] = []
        if db is None:
            print("DatasetRepository: Cannot get datasets, DB connection not available.")
            return briefs

        try:
            cursor = db.DatasetInfoCollection.find()
            datasets_info: list[dict[str, Any]] = [doc for doc in cursor]
            for doc in datasets_info:
                briefs.append(
                    DatasetBrief(
                        dataset_id=str(doc.get('_id')),
                        dataset_name=doc.get('name', 'N/A'),
                        dataset_description=doc.get('description', ''),
                        dataset_type="CSV",
                        dataset_size=doc.get('size', 0)
                    )
                )
        except Exception as e:
            print(f"DatasetRepository: Error fetching dataset briefs from MongoDB: {e}")

        return briefs

    @staticmethod
    def add_dataset(dataset: Dataset) -> ObjectId:
        """
        Добавляет датасет в БД.
        """
        inserted: InsertOneResult = db['DatasetInfoCollection'].insert_one(dataset.to_dict())
        return inserted.inserted_id

    @staticmethod
    def edit_dataset(dataset: Dataset) -> None:
        """
        Изменяет датасет в БД.
        """
        db['DatasetInfoCollection'].update_one(
            {'_id': ObjectId(dataset.dataset_id)},
            {'$set': dataset.to_dict()}
        )

    @staticmethod
    def get_dataset(dataset_id: str) -> Optional[Dataset]:
        """
        Возвращает объект Info для датасета с индексом dataset_id.
        Если датасета с индексом dataset_id нет, то возвращает None.
        """
        collection = db['DatasetInfoCollection']

        dataset = collection.find_one({'_id': ObjectId(dataset_id)})
        if dataset is None:
            raise Exception(f'Element with {dataset_id} not found')

        info: Dataset = Dataset(
            dataset_id,
            dataset['name'],
            dataset['description'],
            dataset['creationDate'],
            dataset['author'],
            dataset['rowCount'],
            dataset['columnCount'],
            dataset['size'],
            dataset['lastVersionNumber'],
            dataset['lastModifiedDate'],
            dataset['path'],
            dataset['lastModifiedBy']
        )
        return info
