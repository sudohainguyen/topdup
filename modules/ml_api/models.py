from typing import Optional

from pydantic import BaseModel


class Entry(BaseModel):
    threshold: int


class QueryResult(BaseModel):
    message: str
    result: str = None
    time: Optional[float] = None