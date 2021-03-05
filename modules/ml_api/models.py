from typing import List

from pydantic import BaseModel


class AllPairsEntry(BaseModel):
    threshold: float = 0.90


class CompareEntry(BaseModel):
    pairs: List[str]


class QueryResult(BaseModel):
    message: str
    result: List[dict] = None
