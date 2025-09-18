"""
User DAO Mongo (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : David Nguyen, 2025
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
from models.user import User

class UserDAOMongo:
    def __init__(self):
        try:
            env_path = ".env"
            print(os.path.abspath(env_path))
            load_dotenv(dotenv_path=env_path)
            db_host = os.getenv("MONGODB_HOST")
            db_name = os.getenv("MYSQL_DB_NAME")
            db_user = os.getenv("DB_USERNAME")
            db_pass = os.getenv("DB_PASSWORD")

            # Verification de connexion
            self.client = MongoClient(
                host=db_host,
                username=db_user,
                password=db_pass,
            )
            self.db = self.client[db_name]
            self.col = self.db["users"]
            self.counters = self.db["counters"]

            # Initialiser le compteur si nécessaire
            self.counters.update_one(
                {"_id": "users"},
                {"$setOnInsert": {"seq": 0}},
                upsert=True
            )
        except FileNotFoundError as e:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur : " + str(e))

    def next_id(self) -> int:
        """
        Emule un auto-increment pour MongoDB
        """
        doc = self.counters.find_one_and_update(
            {"_id": "users"},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return int(doc["seq"])
    
    def select_all(self):
        """
        Return List[User]. Supports docs that use either `_id` (int) or `id` (int).
        """
        rows = self.col.find({}, {"_id": 1, "id": 1, "name": 1, "email": 1})
        result = []
        for doc in rows:
            # Prefer `_id` (Mongo default); fallback to `id` if legacy docs exist
            uid = doc.get("_id")
            if uid is None:
                uid = doc.get("id")
            result.append(User(int(uid) if uid is not None else None,
                               doc.get("name"), doc.get("email")))
        return result
    
    def insert(self, user: User):
        """
        Insert given user into MongoDB.
        """
        # Si pas d'id fourni, on genere un int auto-increment
        uid = int(user.id) if getattr(user, 'id', None) is not None else self.next_id()
        doc = {
            "_id": uid,
            "name": user.name,
            "email": user.email
        }
        self.col.insert_one(doc)
        return uid

    def update(self, user: User) -> int:
        """
        Update given user in MongoDB.
        """
        if not user.id:
            raise ValueError("User ID is required for update operation.")
        doc = {
            "name": user.name,
            "email": user.email
        }
        result = self.col.update_one({"_id": int(user.id)}, {"$set": doc})
        return result.modified_count
    
    def delete(self, user_id: int) -> int:
        """
        Delete user from MongoDB with given user ID.
        """
        result = self.col.delete_one({"_id": int(user_id)})
        return result.deleted_count
    
    def delete_all(self):
        """
        Empty users collection in MongoDB.
        """
        self.col.delete_many({})
        self.counters.update_one(
            {"_id": "users"},
            {"$set": {"seq": 0}},
            upsert=True
        )