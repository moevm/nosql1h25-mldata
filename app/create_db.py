import os

import bson
import pymongo
import datetime
import uuid

import matplotlib.pyplot as plt
from werkzeug.security import generate_password_hash

uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

client = pymongo.MongoClient(uri)
client.admin.command('ping')

db = client.gakkle


def add_examples() -> None:
    db.DatasetInfo.insert_one({
        "DatasetInfo": {
            "_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
            "name": "Sales Data 2023",
            "description": "This dataset contains information about sales",
            "creationDate": datetime.datetime(2023, 7, 15, 9, 30, 45),
            "author": "John Sales",
            "rowCount": 12500,
            "columnCount": 24,
            "size": 5242880,
            "path": "/datasets/sales/dataset.csv",
            "lastVersionNumber": 5,
            "lastModifiedDate": datetime.datetime(2023, 9, 20, 14, 15, 22),
            "lastModifiedBy": "Jane Sales"
        }
    })

    db.DatasetActivity.insert_many([
        {
            "_id": "b2c3d4e5-f6g7-8910-h1i2-j3k4l5m6n7o8",
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
        }
    ])

    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.savefig('test.svg')

    with open('test.svg', 'rb') as f:
        db.DatasetGraphs.insert_one({
            "_id": "b2c3nmn5-f6v7-8g10-hle2-j314l5m5n7o8",
            "graphs": [
                {
                    "name": "Январь",
                    "data": bson.Binary(f.read())
                }
            ]
        })

    db.User.insert_one({
        "_id": "c3d4e5f6-g7h8-9123-i4j5-k6l7m8n9o0p1",
        "username": "John Sales",
        "login": "john.sales@company.com",
        "password": "pa$$word123",
        "status": 1,
        "createdDatasetsCount": 17,
        "accountCreationDate": datetime.datetime(2022, 3, 15, 8, 12, 33),
        "lastAccountModificationDate": datetime.datetime(2023, 10, 28, 14, 45, 21)
    })

    # Admin 
    admin_id = "c3d4e5f6-g7h8-9123-i4j5-k6l7m8n9o0p0"
    admin_pass_hash = generate_password_hash("0dhABEwrwWvtZJQw3aOA1IliEVbiQvWd")
    db.User.update_one(
        {"_id": admin_id},
        {"$set": {
            "username": "Administrator",
            "login": "administrator",
            "password": admin_pass_hash,
            "status": 0,
            "createdDatasetsCount": 0,
            "accountCreationDate": datetime.datetime.now(datetime.timezone.utc),
            "lastAccountModificationDate": datetime.datetime.now(datetime.timezone.utc)
        }},
        upsert=True
    )
    print(f"Upserted Admin User with login: administrator, _id: {admin_id}")

    # Regular User
    user_id = "c3d4e5f6-g7h8-9123-i4j5-k6l7m8n9o0p1"
    user_pass_hash = generate_password_hash("AuQ5UIkdEiQ0tpH8")
    db.User.update_one(
        {"_id": user_id},
        {"$set": {
            "username": "Vasily Pupkin",
            "login": "vasily",
            "password": user_pass_hash,
            "status": 1,
            "createdDatasetsCount": 1,
            "lastAccountModificationDate": datetime.datetime.now(datetime.timezone.utc)
        },
         "$setOnInsert": {
             "accountCreationDate": datetime.datetime(2022, 3, 15, 8, 12, 33, tzinfo=datetime.timezone.utc)
         }},
        upsert=True
    )
    print(f"Upserted Regular User with login: vasily, _id: {user_id}")


if __name__ == '__main__':
    client.drop_database('gakkle')
    add_examples()
