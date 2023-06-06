import pydantic
from bson import ObjectId
from dotenv import dotenv_values
from pymongo import MongoClient


class DBClient:
    def __init__(self) -> None:
        print("Initializing DBClient")

        pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
        env = dotenv_values()

        DB_URI = env.get("DB_URI", None)
        if DB_URI is None:
            raise Exception("DB_URI is not defined")

        self.client = MongoClient(DB_URI)
        self.db = self.client

    def get_leading_offerts(self, offset: int = 0, limit: int = 10) -> list:
        db_curosr = (
            self.db.offerts.offerts.find(
                {},
                {
                    "technologies": 1,
                    "title": 1,
                    "company": 1,
                    "createdAt": 1,
                    "employment_type": 1,
                },
            )
            .skip(offset)
            .limit(limit)
        )

        return list(db_curosr)
