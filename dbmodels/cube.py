from sqlalchemy import Column
from sqlalchemy.types import Numeric, Integer, String, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Cube(Base):
    __tablename__ = 'cubes'
    sn = Column(String(255), primary_key=True)
    name = Column(String(20))
    brand = Column(String(20))
    category = Column(Enum('speed', 'collection'))
    difficulty = Column(Enum('easy','not too easy', 'hard'))
    numofpieces = Column(Integer)
    review = Column(String(255))
    price = Column(Numeric)
