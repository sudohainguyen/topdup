from typing import List

from pydantic import BaseModel


class CompareEntry(BaseModel):
    mode: str
    pairs: List[str]


class QueryResult(BaseModel):
    message: str
    results: dict = None
