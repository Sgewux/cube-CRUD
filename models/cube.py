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


# Pydantic models/schemas
class BaseCube(BaseModel):
    Category: _Category = Field(...)
    Brand: str = Field(..., max_length=20)
    NumOfPieces: Optional[int] = Field(default=None, gt=0)
    Difficulty: _Difficulty = Field(...)
    Review: str = Field(..., min_length=15, max_length=255)
    Price: Optional[float] = Field(default=None, gt=0)


class CubeIn(BaseCube):
    Name: str = Field(..., max_length=20)


class CubeOut(BaseCube):
    Name: str = Field(..., max_length=20)
    SN: str 

