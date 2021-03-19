from typing import List

from pydantic import BaseModel


class CompareSingleEntry(BaseModel):
    mode: str
    content: str


class CompareEntry(BaseModel):
    pairs: List[CompareSingleEntry]


class QueryResult(BaseModel):
    message: str
    results: dict = None
