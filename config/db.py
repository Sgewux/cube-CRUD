import os

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(f'postgresql+psycopg2://postgres:{os.getenv("DBPASSWD")}@localhost:5432/cubecrud')
connection = engine.connect()
