import pydantic

from bson import ObjectId
from dotenv import dotenv_values
from pymongo import MongoClient, UpdateOne
from datetime import datetime


class DBClient:
    def __init__(self) -> None:
        pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

        print("Initializing DBClient")

        env = dotenv_values()

        DB_URI = env.get("DB_URI", None)
        if DB_URI is None:
            raise Exception("DB_URI is not defined")

        # |-- self
        self.client = MongoClient(DB_URI)
        self.db = self.client
        self.migrate()

        print("DBClient initialized")

    def migrate(self) -> None:
        self.db.offerts.dev.create_index(
            [("title", 1), ("company.name", 1)], unique=True
        )

    def insert_offerts(self, offerts: list) -> None:
        self.db.offerts.dev.bulk_write(
            [
                UpdateOne(
                    {
                        "title": offert["title"],
                        "company.name": offert["company"]["name"],
                    },
                    {
                        "$set": {**offert, "updatedAt": datetime.now()},
                        "$setOnInsert": {"createdAt": datetime.now()},
                    },
                    upsert=True,
                )
                for offert in offerts
            ]
        )
        print(f"Successfully inserted [{len(offerts)}] offerts")
