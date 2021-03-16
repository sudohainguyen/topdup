from typing import List

from pydantic import BaseModel


class CompareEntry(BaseModel):
    pairs: List[str]


class QueryResult(BaseModel):
    message: str
    result: List[dict] = None
