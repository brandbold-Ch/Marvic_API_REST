from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()

engine = create_engine(os.getenv("URL_DATABASE"))
Session: sessionmaker = sessionmaker(bind=engine)
Base: DeclarativeMeta = declarative_base()
