"""
Содержит репозиторий для работы с данными пользователей в БД.
"""
import os
import pymongo

from src.models.user import User


uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = pymongo.MongoClient(uri)
db = None

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB.")
    db_name = os.getenv('MONGO_DB_NAME')
    db = client[db_name]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None


class UserRepository:
    """
    Класс-репозиторий для данных, связанных с пользователями.
    """

    @staticmethod
    def find_by_login(login: str) -> User | None:
        """
        Ищет пользователя по логину.
        Возвращает объект User или None, если пользователь не найден или DB недоступна.
        """
        if db is None:
            print("UserRepository: Database connection not available.")
            return None
        try: 
            user_data = db.User.find_one({"login": login})
            if user_data:
                return User(user_data)
        except Exception as e:
            print(f"UserRepository: Error finding user by login '{login}': {e}")
        return None

    @staticmethod
    def find_by_id(user_id: str) -> User | None:
        """
        Ищет пользователя по ID (_id).
        ID должен быть строкой.
        Возвращает объект User или None, если пользователь не найден или DB недоступна.
        """
        if db is None:
            print("UserRepository: Database connection not available.")
            return None
        try:
            user_data = db.User.find_one({"_id": user_id})

            if user_data:
                return User(user_data)
        except Exception as e:
             print(f"UserRepository: Error finding user by id '{user_id}': {e}")
        return None