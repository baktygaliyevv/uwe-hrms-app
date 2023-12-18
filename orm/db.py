from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os

DATABASE_URI = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URI, echo=os.getenv('DEBUG') == '1')

def sessionFactory():
    return Session(engine)