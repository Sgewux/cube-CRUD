from uuid import UUID
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

#Enums
class _Category(Enum):
    speed = 'speed'
    collection = 'collection'


class _Difficulty(Enum):
    easy = 'easy'
    not_too_easy= 'not too easy'
    hard = 'hard'


#Pydantic models/schemas
class CubeIn(BaseModel):
    Name: str = Field(..., max_length=50)
    Category: _Category = Field(...)
    Brand: str = Field(..., max_lenght=50)
    NumOfPieces: Optional[int] = Field(default=None, gt=0)
    Difficulty: _Difficulty = Field(...)
    Review: str = Field(..., min_lenght=15, max_lenght=255)
    Price: Optional[float] = Field(default=None)

class CubeOut(CubeIn):
    SN: str
    
