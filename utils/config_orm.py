from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os


url = URL.create(
    drivername="postgresql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DATABASE"),
    port=os.getenv("DB_PORT")
)

engine = create_engine(url)
SessionLocal: sessionmaker = sessionmaker(bind=engine)
Base: DeclarativeMeta = declarative_base()
