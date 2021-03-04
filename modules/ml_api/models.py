from typing import Optional

from pydantic import BaseModel


class AllPairsEntry(BaseModel):
    threshold: float


class CompareEntry(BaseModel):
    pairs: list[str]


class Result(BaseModel):
    message: str
    result: list = None
