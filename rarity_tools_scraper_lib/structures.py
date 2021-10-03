from pydantic import BaseModel


class Collectable(BaseModel):
    rank: int
    score: float
