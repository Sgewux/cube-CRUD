import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

engine = create_engine(
    f'postgresql+psycopg2://postgres:{os.getenv("DBPASSWD")}@localhost:5432/cubecrud',
    echo=True
)

Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()
