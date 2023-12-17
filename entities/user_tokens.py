from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class UserToken(Base):
    __tablename__ = 'user_tokens'

    token = Column(String(64, 'utf8mb3_unicode_ci'), primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    expiration_date = Column(DateTime, nullable=False)

    user = relationship('User')
