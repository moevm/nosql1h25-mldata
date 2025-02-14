import os
from urllib.parse import quote_plus

import pymongo
import pytest


@pytest.fixture(scope="session")
def mongodb():
    user = os.environ["USR"]
    password = os.environ["PWD"]
    host = os.environ["HOST"]

    uri = "mongodb://%s:%s@%s" % (
        quote_plus(user), quote_plus(password), host)

    client = pymongo.MongoClient(uri)

    assert client.admin.command("ping")["ok"] != 0.0
    return client


def test_update_mongodb(mongodb):
    db_name = os.environ["DB_NAME"]
    db = mongodb[db_name]

    db['test_col'].insert_one(
        {
            "_id":         "bad_document",
            "description": "Content of the document",
        }
    )

    print('\n', '>' * 5, db['test_col'].find_one({"_id": "bad_document"}))

    db['test_col'].delete_one({"_id": "bad_document"})

    print('\n', '>' * 5, db['test_col'].find_one({"_id": "bad_document"}))


def test_mongodb_fixture(mongodb):
    assert mongodb.admin.command("ping")["ok"] > 0
