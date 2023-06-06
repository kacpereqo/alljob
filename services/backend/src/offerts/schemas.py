from common.schemas.offerts import Filter, Filtering, Sorting, Technology
from pydantic import validator


class Sorting(Sorting):
    @validator("orderBy")
    def is_correct_ordered(cls, v):
        order = {"asc": 1, "desc": -1}
        if v not in order.keys():
            raise ValueError("orderBy must be either 'asc' or 'desc'")
        else:
            return order[v]

    @validator("sortBy")
    def is_correct_named(cls, v):
        sorters = ("date", "salary", "distance")

        if v not in sorters:
            raise ValueError(f"sortBy must be one of the following: {sorters}")
        else:
            return v


class Filter(Filter):
    pass


class Technology(Technology):
    pass


class Filtering(Filtering):
    pass
