from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'sqlite:///your_database.db'  # our database URI

engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Session = scoped_session(SessionLocal)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
