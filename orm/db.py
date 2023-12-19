from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os

def init_db():
    global DATABASE_URI
    global engine
    global session

    DATABASE_URI = os.getenv('DATABASE_URL')
    engine = create_engine(DATABASE_URI, echo=os.getenv('DEBUG') == '1')
    session = Session(engine)