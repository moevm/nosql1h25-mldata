import os

import bson
import pymongo
import datetime
import shutil

import matplotlib.pyplot as plt

from bson import ObjectId
from pathlib import Path
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash


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
    if not db.DatasetInfoCollection.find({"_id": {"$in": ["b2c3d4e5-0000-0000-h1i2-j3k4l5m6n7o8", "b2c3d4e5-f6g7-8910-1111-j3k4l5m6n7o8", "b2c774e5-f6g7-8910-h1i2-j3ktttm6nqrr"]}}).to_list():
        shutil.copytree("/app/example-datasets", "/app/datasets", dirs_exist_ok=True)
        db.DatasetInfoCollection.insert_many([
            {
                "_id": "b2c3d4e5-0000-0000-h1i2-j3k4l5m6n7o8",
                "name": "Example dataset 1",
                "description": "This dataset is used for debugging",
                "creationDate": datetime.datetime(2023, 7, 15, 9, 30, 45),
                "author": "John Sales",
                "rowCount": 10,
                "columnCount": 2,
                "size": 0.05,
                "path": "./datasets",
                "lastVersionNumber": 1,
                "lastModifiedDate": datetime.datetime(2023, 9, 20, 14, 15, 22),
                "lastModifiedBy": "Jane Sales"
            },
            {
                "_id": "b2c3d4e5-f6g7-8910-1111-j3k4l5m6n7o8",
                "name": "Example dataset 2",
                "description": "This dataset is used for debugging",
                "creationDate": datetime.datetime(2021, 7, 15, 9, 30, 45),
                "author": "John Sales",
                "rowCount": 10,
                "columnCount": 2,
                "size": 0.05,
                "path": "./datasets",
                "lastVersionNumber": 1,
                "lastModifiedDate": datetime.datetime(2021, 9, 20, 14, 15, 22),
                "lastModifiedBy": "Jane Sales"
            },
            {
                "_id": "b2c774e5-f6g7-8910-h1i2-j3ktttm6nqrr",
                "name": "Another dataset 3",
                "description": "This dataset is used for debugging",
                "creationDate": datetime.datetime(2022, 7, 15, 9, 30, 45),
                "author": "John Sales",
                "rowCount": 10,
                "columnCount": 2,
                "size": 0.05,
                "path": "./datasets",
                "lastVersionNumber": 1,
                "lastModifiedDate": datetime.datetime(2023, 9, 20, 14, 15, 22),
                "lastModifiedBy": "Jane Sales"
            }
        ])

    if not db.DatasetActivity.find({"_id": {"$in": ["b2c3d4e5-0000-0000-h1i2-j3k4l5m6n7o8", "b2c3d4e5-f6g7-8910-1111-j3k4l5m6n7o8", "b2c774e5-f6g7-8910-h1i2-j3ktttm6nqrr"]}}).to_list():
        db.DatasetActivity.insert_many([
            {
                "_id": "b2c3d4e5-0000-0000-h1i2-j3k4l5m6n7o8",
                "statistics": {
                    "2023-10-01": {
                        "views": 42,
                        "downloads": 7
                    },
                    "2023-10-02": {
                        "views": 38,
                        "downloads": 5
                    },
                    "2023-10-03": {
                        "views": 55,
                        "downloads": 12
                    },
                    "2023-10-04": {
                        "views": 61,
                        "downloads": 9
                    },
                    "2023-10-05": {
                        "views": 47,
                        "downloads": 8
                    },
                    "2023-10-06": {
                        "views": 72,
                        "downloads": 15
                    },
                    "2023-10-07": {
                        "views": 89,
                        "downloads": 21
                    },
                    "2023-10-08": {
                        "views": 65,
                        "downloads": 14
                    },
                    "2023-10-09": {
                        "views": 53,
                        "downloads": 11
                    },
                    "2023-10-10": {
                        "views": 48,
                        "downloads": 7
                    },
                    "2023-10-11": {
                        "views": 57,
                        "downloads": 10
                    },
                    "2023-10-12": {
                        "views": 62,
                        "downloads": 13
                    },
                    "2023-10-13": {
                        "views": 71,
                        "downloads": 16
                    },
                    "2023-10-14": {
                        "views": 84,
                        "downloads": 19
                    },
                    "2023-10-15": {
                        "views": 76,
                        "downloads": 18
                    },
                    "2023-10-16": {
                        "views": 59,
                        "downloads": 12
                    },
                    "2023-10-17": {
                        "views": 63,
                        "downloads": 11
                    },
                    "2023-10-18": {
                        "views": 67,
                        "downloads": 14
                    },
                    "2023-10-19": {
                        "views": 72,
                        "downloads": 16
                    },
                    "2023-10-20": {
                        "views": 81,
                        "downloads": 20
                    },
                    "2023-10-21": {
                        "views": 93,
                        "downloads": 25
                    },
                    "2023-10-22": {
                        "views": 87,
                        "downloads": 22
                    },
                    "2023-10-23": {
                        "views": 79,
                        "downloads": 18
                    },
                    "2023-10-24": {
                        "views": 68,
                        "downloads": 15
                    },
                    "2023-10-25": {
                        "views": 74,
                        "downloads": 17
                    },
                    "2023-10-26": {
                        "views": 82,
                        "downloads": 19
                    },
                    "2023-10-27": {
                        "views": 91,
                        "downloads": 23
                    },
                    "2023-10-28": {
                        "views": 95,
                        "downloads": 26
                    },
                    "2023-10-29": {
                        "views": 88,
                        "downloads": 24
                    },
                    "2023-10-30": {
                        "views": 77,
                        "downloads": 21
                    }
                }
            },
            {
                "_id": "b2c3d4e5-f6g7-8910-1111-j3k4l5m6n7o8",
                "statistics": {
                    "2023-10-01": {
                        "views": 42,
                        "downloads": 799
                    },
                    "2023-10-02": {
                        "views": 6668,
                        "downloads": 5
                    }
                }
            },
            {
                "_id": "b2c774e5-f6g7-8910-h1i2-j3ktttm6nqrr",
                "statistics": {
                    "2023-10-01": {
                        "views": 42,
                        "downloads": 799
                    },
                    "2023-10-02": {
                        "views": 6668,
                        "downloads": 5
                    }
                }
            },
        ])

    if not db.DatasetGraphs.find({"_id": {"$in": ["b2c3d4e5-0000-0000-h1i2-j3k4l5m6n7o8", "b2c3d4e5-f6g7-8910-1111-j3k4l5m6n7o8", "b2c774e5-f6g7-8910-h1i2-j3ktttm6nqrr"]}}).to_list():

        plt.plot([1, 2, 3, 4])
        plt.ylabel('some numbers')
        plt.savefig('test.svg')

        with open('test.svg', 'rb') as f:
            db.DatasetGraphs.insert_many([
                {
                    "_id": "b2c3d4e5-0000-0000-h1i2-j3k4l5m6n7o8",
                    "graphs": [
                        {
                            "name": "Январь",
                            "data": bson.Binary(f.read())
                        }
                    ]
                },
                {
                    "_id": "b2c3d4e5-f6g7-8910-1111-j3k4l5m6n7o8",
                    "graphs": [
                        {
                            "name": "Январь",
                            "data": bson.Binary(f.read())
                        }
                    ]
                },
                {
                    "_id": "b2c774e5-f6g7-8910-h1i2-j3ktttm6nqrr",
                    "graphs": [
                        {
                            "name": "Январь",
                            "data": bson.Binary(f.read())
                        }
                    ]
                }
            ])

    if not db.User.find_one({"_id": "c3d4e5f6-g7h8-9123-i4j5-k6l7m8n9o0p1"}):
        john_pass_hash = generate_password_hash("pa$$word123")
        db.User.insert_one({
            "_id": "c3d4e5f6-g7h8-9123-i4j5-k6l7m8n9o0p1",
            "username": "John Sales",
            "login": "john.sales@company.com",
            "password": john_pass_hash,
            "status": 1,
            "createdDatasetsCount": 17,
            "accountCreationDate": datetime.datetime(2022, 3, 15, 8, 12, 33),
            "lastAccountModificationDate": datetime.datetime(2023, 10, 28, 14, 45, 21)
        })

    # Admin 
    admin_id = "c3d4e5f6-g7h8-9123-i4j5-k6l7m8n9o0p0"
    if not db.User.find_one({"_id": admin_id}):
        admin_pass_hash = generate_password_hash("0dhABEwrwWvtZJQw3aOA1IliEVbiQvWd")
        db.User.insert_one({
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
    if not db.User.find_one({"_id": user_id}):
        user_pass_hash = generate_password_hash("AuQ5UIkdEiQ0tpH8")
        db.User.insert_one({
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
