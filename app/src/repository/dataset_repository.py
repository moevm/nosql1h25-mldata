"""
Содержит репозитории приложения.
Репозиторий напрямую работает с БД - добавляет, изменяет, удаляет и ищет записи в БД.
"""
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime, timedelta
from glob import glob
from io import BytesIO
from typing import Any
from typing import Optional, Tuple

import pymongo
from flask import current_app, g
from flask_pymongo import PyMongo
from pymongo.results import InsertOneResult
from werkzeug.datastructures import FileStorage
from werkzeug.local import LocalProxy

from src.models.Dataset import Dataset
from src.models.DatasetBrief import DatasetBrief
from src.models.FilterValues import FilterValues

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
    def get_filtered_briefs(filters: FilterValues) -> list:
        query: dict = {}

        if filters.name:
            name_regex = re.compile(f'.*{re.escape(filters.name)}.*', re.IGNORECASE)
            query['name'] = {'$regex': name_regex}

        if filters.size_from is not None or filters.size_to is not None:
            query['size'] = DatasetRepository._create_from_to_query(filters.size_from, filters.size_to)

        if filters.row_size_from is not None or filters.row_size_to is not None:
            query['rowCount'] = DatasetRepository._create_from_to_query(filters.row_size_from, filters.row_size_to)

        if filters.column_size_from is not None or filters.column_size_to is not None:
            query['columnCount'] = DatasetRepository._create_from_to_query(filters.column_size_from,
                                                                           filters.column_size_to)

        if filters.creation_date_from is not None or filters.creation_date_to is not None:
            query['creationDate'] = DatasetRepository._create_from_to_query(filters.creation_date_from,
                                                                            filters.creation_date_to)

        if filters.modify_date_from is not None or filters.modify_date_to is not None:
            query['lastModifiedDate'] = DatasetRepository._create_from_to_query(filters.modify_date_from,
                                                                                filters.modify_date_to)

        sort_query: list = []
        if filters.sort is not None:
            sort_query.append((filters.sort['field'], 1 if filters.sort['order'] == 'asc' else -1))

        cursor = db['DatasetInfoCollection'].find(query).sort(sort_query)

        briefs: list = []
        for doc in cursor:
            briefs.append(
                DatasetBrief(
                    dataset_id=str(doc.get('_id')),
                    dataset_name=doc.get('name', 'N/A'),
                    dataset_description=doc.get('description', ''),
                    dataset_type="CSV",
                    dataset_size=doc.get('size', 0)
                )
            )

        return briefs

    @staticmethod
    def add_dataset(dataset: Dataset) -> str:
        """
        Добавляет датасет в БД.
        """
        # потенциально может случиться такое, что uuid нагенерит два одинаковых id
        # и тут из-за этого все упадет
        # надо обернуть в try-catch и в блоке catch перегенерить id
        inserted: InsertOneResult = db['DatasetInfoCollection'].insert_one(dataset.to_dict())
        return inserted.inserted_id

    @staticmethod
    def edit_dataset(dataset: Dataset) -> None:
        """
        Изменяет датасет в БД.
        """
        db['DatasetInfoCollection'].update_one(
            {'_id': dataset.dataset_id},
            {'$set': dataset.to_dict()}
        )

    @staticmethod
    def get_dataset(dataset_id: str) -> Optional[Dataset]:
        """
        Возвращает объект Info для датасета с индексом dataset_id.
        Если датасета с индексом dataset_id нет, то возвращает None.
        """
        collection = db['DatasetInfoCollection']

        dataset = collection.find_one({'_id': dataset_id})
        if dataset is None:
            raise Exception(f'Element with {dataset_id} not found')

        info: Dataset = Dataset(dataset_id, dataset['name'], dataset['description'], dataset['creationDate'],
                                dataset['author'], dataset['rowCount'], dataset['columnCount'], dataset['size'],
                                dataset['lastVersionNumber'], dataset['lastModifiedDate'], dataset['path'],
                                dataset['lastModifiedBy'])
        return info

    @staticmethod
    def remove_dataset(dataset_id: str) -> None:
        """
        Удаляет датасет из БД.
        """
        db['DatasetInfoCollection'].delete_one(
            {'_id': dataset_id},
        )

    @staticmethod
    def export_datasets_archive() -> Tuple[BytesIO, str]:
        temp_dir = tempfile.mkdtemp()

        try:
            # Создаем временную структуру директорий
            db_dump_dir = os.path.join(temp_dir, "mongodb_dump")
            csv_dir = os.path.join(temp_dir, "datasets")
            datasets_dir = "/app/datasets"

            os.makedirs(db_dump_dir, exist_ok=True)
            os.makedirs(csv_dir, exist_ok=True)

            # 1. Делаем mongodump
            mongodump_cmd = [
                "mongodump",
                "--uri", uri,
                "--out", db_dump_dir
            ]
            subprocess.run(mongodump_cmd, check=True)

            # 2. Конвертируем BSON → JSON через bsondump
            bson_files = glob(os.path.join(db_dump_dir, db_name, "*.bson"))
            for bson_file in bson_files:
                json_file = bson_file.replace(".bson", ".json")
                subprocess.run(["bsondump", "--pretty", "--outFile", json_file, bson_file], check=True)

            # 3. Копируем CSV файлы в отдельную директорию
            if os.path.exists(datasets_dir):
                for csv_file in glob(os.path.join(datasets_dir, "*.csv")):
                    shutil.copy2(
                        csv_file,
                        os.path.join(csv_dir, os.path.basename(csv_file))
                    )

            # 4. Создаем ZIP-архив с правильной структурой
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Сохраняем файлы с относительными путями внутри архива
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)

            zip_buffer.seek(0)
            return zip_buffer, f'dump_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'

        finally:
            # Очищаем временные файлы
            shutil.rmtree(temp_dir, ignore_errors=True)

    @staticmethod
    def import_datasets_archive(backup: FileStorage) -> None:
        temp_dir = tempfile.mkdtemp()

        try:
            # Сохраняем архив
            backup_path = os.path.join(temp_dir, backup.filename)
            backup.save(backup_path)

            # Распаковываем
            with zipfile.ZipFile(backup_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            db_dump_dir = os.path.join(temp_dir, "mongodb_dump", db_name)
            csv_dir = os.path.join(temp_dir, "datasets")
            datasets_dir = "/app/datasets"

            # Удаляем старые CSV
            for item in os.listdir(datasets_dir):
                os.remove(os.path.join(datasets_dir, item))

            # Копируем новые
            if os.path.exists(csv_dir):
                for item in os.listdir(csv_dir):
                    shutil.copy2(os.path.join(csv_dir, item), os.path.join(datasets_dir, item))

            # Восстановление MongoDB
            cmd = [
                'mongorestore',
                '--uri', uri,
                '--drop',
                db_dump_dir
            ]
            subprocess.run(cmd, check=True)

        finally:
            # Очищаем временные файлы
            shutil.rmtree(temp_dir, ignore_errors=True)

    @staticmethod
    def _create_from_to_query(from_: Optional[int | float | datetime], to_: Optional[int | float | datetime]) -> dict:
        INT64_MAX: int = 9223372036854775807
        DATETIME_MAX: datetime = datetime.today() + timedelta(days=1)

        query: dict = {}
        if from_ is not None:
            if isinstance(from_, datetime):
                query['$gte'] = min(from_, DATETIME_MAX)
            else:
                query['$gte'] = min(from_, INT64_MAX)
        if to_ is not None:
            if isinstance(to_, datetime):
                query['$lte'] = min(to_ + timedelta(days=1), DATETIME_MAX)
            else:
                query['$lte'] = min(to_, INT64_MAX)
        return query
