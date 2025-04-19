import os
import pymongo
import pytest

from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()


@pytest.fixture(scope="session")
def mongodb():
    user = os.getenv("MONGO_ROOT_USER")
    password = os.getenv("MONGO_ROOT_PASS")
    host = os.getenv("HOST")
    port = os.getenv("PORT")

    uri = f"mongodb://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}"

    client = pymongo.MongoClient(uri)

    assert client.admin.command("ping")["ok"] != 0.0
    return client


def test_update_mongodb(mongodb):
    db_name = os.environ["MONGO_DB_NAME"]
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
