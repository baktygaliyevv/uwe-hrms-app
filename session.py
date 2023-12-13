from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URL')

SECRET_KEY = os.getenv('SECRET_KEY')

engine = create_engine(DATABASE_URI, echo=os.getenv('DEBUG') == '1')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
