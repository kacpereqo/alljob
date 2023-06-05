import pydantic
from bson import ObjectId
from dotenv import dotenv_values
from pymongo import MongoClient


class DBClient:
    def __init__(self) -> None:
        pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

        print("Initializing DBClient")

        env = dotenv_values()

        DB_URI = env.get("DB_URI", None)
        if DB_URI is None:
            raise Exception("DB_URI is not defined")

        self.client = MongoClient(DB_URI)
        self.db = self.client

    def get_leading_offerts(self) -> list:
        return self.db.offerts.offerts.find_one()
