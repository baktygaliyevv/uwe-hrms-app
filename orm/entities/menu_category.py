# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MenuCategory(Base):
    __tablename__ = 'menu_categories'

    id = Column(Integer, primary_key=True)
    name = Column(Text(collation='utf8mb3_unicode_ci'), nullable=False)