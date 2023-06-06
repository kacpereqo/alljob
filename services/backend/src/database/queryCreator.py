from abc import ABC, abstractmethod


def sorting_query_creator(sorting):
    query_creators = {
        "date": DateQueryCreator,
        "salary": SalaryQueryCreator,
        "distance": DistanceQueryCreator,
    }
    query_creator = query_creators.get(sorting.sortBy, None)

    if query_creator is None:
        raise Exception("query_creator is None")

    return query_creator.create_query(sorting.orderBy)


class QueryCreator(ABC):
    @abstractmethod
    def create_query(sortBy: str) -> dict:
        pass


class DateQueryCreator(QueryCreator):
    def create_query(sortBy) -> dict:
        return [
            {
                "$project": {
                    "technologies": 1,
                    "title": 1,
                    "company": 1,
                    "createdAt": 1,
                    "employmentTypes": 1,
                }
            },
            {"$sort": {"createdAt": sortBy}},
        ]


class SalaryQueryCreator(QueryCreator):
    def create_query(sortBy):
        return [
            {"$unwind": {"path": "$employmentTypes"}},
            {"$match": {"employmentTypes.salary": {"$exists": True}}},
            {
                "$group": {
                    "_id": "$_id",
                    "min": {"$min": "$employmentTypes.salary.pln.from"},
                    "technologies": {"$first": "$technologies"},
                    "title": {"$first": "$title"},
                    "company": {"$first": "$company"},
                    "createdAt": {"$first": "$createdAt"},
                    "employmentTypes": {"$push": "$employmentTypes"},
                }
            },
            {
                "$sort": {"min": sortBy},
            },
        ]


class DistanceQueryCreator(QueryCreator):
    def create_query(sortBy):
        return ""
