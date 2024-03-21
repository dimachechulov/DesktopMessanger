from datetime  import datetime

from sqlalchemy import MetaData, Integer, TIMESTAMP, String, Table, Column, create_engine, UniqueConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

from configs.default import SENDER

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String)
    age = Column(Integer)
    password = Column(String, nullable=False)
    UniqueConstraint('name')

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    from_user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'),nullable=False)
    to_user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())
    content = Column(String, nullable=False)






