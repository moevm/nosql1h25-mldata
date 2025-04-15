"""
Содержит репозитории приложения. Репозиторий напрямую работает с БД - добавляет, изменяет, удаляет и ищет записи в БД.
"""
import os
import pymongo
from app.src.models.DatasetBrief import DatasetBrief

# --- Database Connection ---
uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
db = None

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB for DatasetRepository.")
    db = client.gakkle
except Exception as e:
    print(f"Error connecting to MongoDB for DatasetRepository: {e}")

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
            cursor = db.DatasetInfo.find(
                {},
                {
                    "_id": 1,
                    "name": 1,
                    "description": 1,
                    "size": 1,
                    "path": 1
                }
            )
            for doc in cursor:
                dataset_type = "Unknown"
                if doc.get("path"):
                    try:
                        ext = os.path.splitext(doc["path"])[1].lower()
                        if ext == ".csv": dataset_type = "CSV"
                        elif ext in [".jpg", ".png", ".svg"]: dataset_type = "Image"
                    except Exception:
                        pass

                briefs.append(
                    DatasetBrief(
                        dataset_id=str(doc.get('_id')),
                        dataset_name=doc.get('name', 'N/A'),
                        dataset_description=doc.get('description', ''),
                        dataset_type=dataset_type,
                        dataset_size=doc.get('size', 0)
                    )
                )
        except Exception as e:
            print(f"DatasetRepository: Error fetching dataset briefs from MongoDB: {e}")

        return briefs