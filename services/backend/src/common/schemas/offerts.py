from typing import List

from pydantic import BaseModel


class Sorting(BaseModel):
    sortBy: str = "date"
    orderBy: str = "desc"


class Filter(BaseModel):
    min_value: int
    max_value: int


class Seniority(BaseModel):
    name: str


class Technology(BaseModel):
    name: str


class WorkingMode(BaseModel):
    name: str


class Filtering(BaseModel):
    salary: Filter | None
    distance: Filter | None
    seniority: List[Seniority] | None
    workingMode: List[WorkingMode] | None
    cities: List[str] | None
    technologies: List[Technology] | None
