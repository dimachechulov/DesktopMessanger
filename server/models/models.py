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


class Query(Base):
    __tablename__ = 'query'
    id = Column(Integer, primary_key=True)
    from_user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    to_user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

class Friend(Base):
    __tablename__ = 'friend'
    id = Column(Integer, primary_key=True)
    user1 = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user2 = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)






