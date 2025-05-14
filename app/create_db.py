import os
import shutil
import pymongo
import datetime

from pathlib import Path
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

from run import app
from src.services.dataset_service import DatasetService


env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

user: str = os.getenv("MONGO_ROOT_USER")
password: str = os.getenv("MONGO_ROOT_PASS")
host: str = os.getenv("HOST")
port: str = os.getenv("PORT")
uri: str = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
db_name: str = os.getenv("MONGO_DB_NAME")

client = pymongo.MongoClient(uri)
client.admin.command('ping')

db = client[db_name]


def add_examples() -> None:
    dataset_id1: str = "b2c3d4e5-0000-0000-h1i2-j3k4l5m6n7o8"
    dataset_id2: str = "b2c3d4e5-f6g7-8910-1111-j3k4l5m6n7o8"
    dataset_id3: str = "b2c774e5-f6g7-8910-h1i2-j3ktttm6nqrr"

    if not db.DatasetInfoCollection.find().to_list():
        shutil.copytree("/app/example-datasets", "/app/datasets", dirs_exist_ok=True)
        db.DatasetInfoCollection.insert_many([
            {
                "_id": dataset_id1,
                "name": "Example dataset 1",
                "description": "This dataset is used for debugging",
                "creationDate": datetime.datetime(2023, 7, 15, 9, 30, 45),
                "author": "John Sales",
                "author_login": "john.sales@company.com",
                "rowCount": 10,
                "columnCount": 2,
                "size": 0.05,
                "path": "./datasets",
                "lastVersionNumber": 1,
                "lastModifiedDate": datetime.datetime(2023, 9, 20, 14, 15, 22),
                "lastModifiedBy": "Jane Sales"
            },
            {
                "_id": dataset_id2,
                "name": "Example dataset 2",
                "description": "This dataset is used for debugging",
                "creationDate": datetime.datetime(2021, 7, 15, 9, 30, 45),
                "author": "John Sales",
                "author_login": "john.sales@company.com",
                "rowCount": 10,
                "columnCount": 2,
                "size": 0.05,
                "path": "./datasets",
                "lastVersionNumber": 1,
                "lastModifiedDate": datetime.datetime(2021, 9, 20, 14, 15, 22),
                "lastModifiedBy": "Jane Sales"
            },
            {
                "_id": dataset_id3,
                "name": "Another dataset 3",
                "description": "This dataset is used for debugging",
                "creationDate": datetime.datetime(2022, 7, 15, 9, 30, 45),
                "author": "John Sales",
                "author_login": "john.sales@company.com",
                "rowCount": 10,
                "columnCount": 2,
                "size": 0.05,
                "path": "./datasets",
                "lastVersionNumber": 1,
                "lastModifiedDate": datetime.datetime(2023, 9, 20, 14, 15, 22),
                "lastModifiedBy": "Jane Sales"
            }
        ])

    if not db.DatasetActivityCollection.find().to_list():
        db.DatasetActivityCollection.insert_many([
            {
                "_id": dataset_id1,
                "statistics": {
                    "2025-04-01": {
                        "views": 42,
                        "downloads": 7
                    },
                    "2025-04-02": {
                        "views": 38,
                        "downloads": 5
                    },
                    "2025-04-03": {
                        "views": 55,
                        "downloads": 12
                    },
                    "2025-04-04": {
                        "views": 61,
                        "downloads": 9
                    },
                    "2025-04-05": {
                        "views": 47,
                        "downloads": 8
                    },
                    "2025-04-06": {
                        "views": 72,
                        "downloads": 15
                    },
                    "2025-04-07": {
                        "views": 89,
                        "downloads": 21
                    },
                    "2025-04-08": {
                        "views": 65,
                        "downloads": 14
                    },
                    "2025-04-09": {
                        "views": 53,
                        "downloads": 11
                    },
                    "2025-04-10": {
                        "views": 48,
                        "downloads": 7
                    },
                    "2025-04-11": {
                        "views": 57,
                        "downloads": 10
                    },
                    "2025-04-12": {
                        "views": 62,
                        "downloads": 13
                    },
                    "2025-04-13": {
                        "views": 71,
                        "downloads": 16
                    },
                    "2025-04-14": {
                        "views": 84,
                        "downloads": 19
                    },
                    "2025-04-15": {
                        "views": 76,
                        "downloads": 18
                    },
                    "2025-04-16": {
                        "views": 59,
                        "downloads": 12
                    },
                    "2025-04-17": {
                        "views": 63,
                        "downloads": 11
                    },
                    "2025-04-18": {
                        "views": 67,
                        "downloads": 14
                    },
                    "2025-04-19": {
                        "views": 72,
                        "downloads": 16
                    },
                    "2025-04-20": {
                        "views": 81,
                        "downloads": 20
                    },
                    "2025-04-21": {
                        "views": 93,
                        "downloads": 25
                    },
                    "2025-04-22": {
                        "views": 87,
                        "downloads": 22
                    },
                    "2025-04-23": {
                        "views": 79,
                        "downloads": 18
                    },
                    "2025-04-24": {
                        "views": 68,
                        "downloads": 15
                    },
                    "2025-04-25": {
                        "views": 74,
                        "downloads": 17
                    },
                    "2025-04-26": {
                        "views": 82,
                        "downloads": 19
                    },
                    "2025-04-27": {
                        "views": 91,
                        "downloads": 23
                    },
                    "2025-04-28": {
                        "views": 95,
                        "downloads": 26
                    },
                    "2025-04-29": {
                        "views": 88,
                        "downloads": 24
                    },
                    "2025-04-30": {
                        "views": 77,
                        "downloads": 21
                    }
                }
            },
            {
                "_id": dataset_id2,
                "statistics": {
                    "2025-05-01": {
                        "views": 42,
                        "downloads": 799
                    },
                    "2025-05-02": {
                        "views": 6668,
                        "downloads": 5
                    }
                }
            },
            {
                "_id": dataset_id3,
                "statistics": {
                    "2025-05-01": {
                        "views": 42,
                        "downloads": 799
                    },
                    "2025-05-02": {
                        "views": 6668,
                        "downloads": 5
                    }
                }
            },
        ])

    if not db.DatasetGraphsCollection.find().to_list():
        with app.app_context():
            for dataset_id in (dataset_id1, dataset_id2, dataset_id3):
                DatasetService.save_plots(dataset_id)

    if not db.UserCollection.find_one({"_id": "c3d4e5f6-g7h8-9123-i4j5-k6l7m8n9o0p1"}):
        john_pass_hash = generate_password_hash("pa$$word123")
        db.UserCollection.insert_one({
            "_id": "c3d4e5f6-g7h8-9123-i4j5-k6l7m8n9o0p1",
            "username": "John Sales",
            "login": "john.sales@company.com",
            "password": john_pass_hash,
            "status": 1,
            "createdDatasetsCount": 3,
            "accountCreationDate": datetime.datetime(2022, 3, 15, 8, 12, 33),
            "lastAccountModificationDate": datetime.datetime(2023, 10, 28, 14, 45, 21)
        })

    # Admin 
    admin_id = "c3d4e5f6-g7h8-9123-i4j5-k6l7m8n9o0p0"
    if not db.UserCollection.find_one({"_id": admin_id}):
        admin_pass_hash = generate_password_hash("0dhABEwrwWvtZJQw3aOA1IliEVbiQvWd")
        db.UserCollection.insert_one({
            "_id": admin_id,
            "username": "Administrator",
            "login": "administrator",
            "password": admin_pass_hash,
            "status": 0,
            "createdDatasetsCount": 0,
            "accountCreationDate": datetime.datetime(2025, 5, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            "lastAccountModificationDate": datetime.datetime(2025, 5, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        })

    # Regular User
    user_id = "09365d4b-af81-42ae-89b8-54f232c0c8fb"
    if not db.UserCollection.find_one({"_id": user_id}):
        user_pass_hash = generate_password_hash("AuQ5UIkdEiQ0tpH8")
        db.UserCollection.insert_one({
            "_id": user_id,
            "username": "Vasily Pupkin",
            "login": "vasily",
            "password": user_pass_hash,
            "status": 1,
            "createdDatasetsCount": 0,
            "accountCreationDate": datetime.datetime(2025, 5, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            "lastAccountModificationDate": datetime.datetime(2025, 5, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        })


if __name__ == '__main__':
    add_examples()
