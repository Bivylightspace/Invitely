from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.sql import func
import hashlib
from sqlalchemy.event import listens_for

Base = declarative_base()

class Invitation(Base):
    __tablename_ = "Invitation"
    ID = Column(Integer, primary_key=True)
    Email = Column(String, nullable=False)
    Password = Column(String)
    Created = Column(DateTime, default=func.now())

class Event(Base):
    __tablename__  = 'events'
    ID = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False) 
    DateTime = Column(DateTime, nullable=False)
    Location = Column(String)


    # @listens_for(Invitation, 'after_insert')
    # def after_insert_invitation(mapper, connection, target):
    # target.Password = hashlib.sha256()     