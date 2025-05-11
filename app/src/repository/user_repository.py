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

    @staticmethod
    def find_by_username(username: str) -> User | None:
        """
        Ищет пользователя по имени пользователя.
        Возвращает объект User или None, если пользователь не найден или DB недоступна.
        """
        if db is None:
            print("UserRepository: Database connection not available.")
            return None
        try:
            user_data = db.User.find_one({"username": username})
            if user_data:
                return User(user_data)
        except Exception as e:
            print(f"UserRepository: Error finding user by username '{username}': {e}")
        return None

    @staticmethod
    def find_by_login(user_login: str) -> User | None:
        """
        Ищет пользователя по логину.
        Возвращает объект User или None, если пользователь не найден или DB недоступна.
        """
        if db is None:
            print("UserRepository: Database connection not available.")
            return None
        try:
            user_data = db.User.find_one({"login": user_login})
            if user_data:
                return User(user_data)
        except Exception as e:
            print(f"UserRepository: Error finding user by login '{user_login}': {e}")
        return None

    @staticmethod
    def update_user_fields(user_id: str, fields_to_update: dict[str, any]) -> bool:
        """
        Обновляет указанные поля для пользователя с данным user_id.
        Возвращает True в случае успеха, False в противном случае.
        """
        if db is None:
            print("UserRepository: Database connection not available for update.")
            return False
        if not fields_to_update:
            return True 

        try:
            result = db.User.update_one({"_id": user_id}, {"$set": fields_to_update})
            return result.modified_count > 0 or (result.matched_count > 0 and not fields_to_update)
        except Exception as e:
            print(f"UserRepository: Error updating user fields for id '{user_id}': {e}")
            return False