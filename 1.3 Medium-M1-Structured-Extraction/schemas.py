from typing import Literal
from pydantic import BaseModel, ValidationError

class ReviewExtract(BaseModel):
    sentiment: Literal['positive', 'negative', 'mixed']
    dishes_mentioned: list[str]
    rating_out_of_5: float