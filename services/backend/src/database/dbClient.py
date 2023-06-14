from datetime import datetime
from typing import List

import pydantic
import os

from bson import ObjectId
from common.schemas.offerts import Filtering, Sorting
from database.queryCreator import sorting_query_creator
from pymongo import MongoClient, UpdateOne


class DBClient:
    def __init__(self) -> None:
        pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

        DB_URI = os.environ.get("DB_URI", None)
        if DB_URI is None:
            raise Exception("DB_URI is not defined")

        self.client = MongoClient(DB_URI)
        self.db = self.client
        self.migrate()

    def migrate(self) -> None:
        self.db.offerts.offerts.create_index(
            [("title", 1), ("company.name", 1)], unique=True
        )

    def insert_offerts(self, offerts: list) -> None:
        self.db.offerts.offerts.bulk_write(
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

    def get_leading_offerts(
        self,
        offset: int = 0,
        limit: int = 10,
        sorting: Sorting = None,
        filtering: Filtering = None,
    ) -> List:
        query = []

        if sorting is not None:
            query.extend(sorting_query_creator(sorting))
        else:  # sorting is None
            query.extend(
                [
                    {
                        "$project": {
                            "technologies": 1,
                            "title": 1,
                            "company": 1,
                            "createdAt": 1,
                            "employmentTypes": 1,
                            "locations": 1,
                        }
                    },
                    {"$sort": {"createdAt": 1}},
                ]
            )

        # offset and limit
        query.append({"$skip": offset})
        query.append({"$limit": limit})

        return list(self.db.offerts.offerts.aggregate(query))

    def get_offert_details(self, offert_id: str) -> dict:
        return self.db.offerts.offerts.find_one({"_id": ObjectId(offert_id)})

    def get_offerts_count(self) -> int:
        return self.db.offerts.offerts.count_documents({})
