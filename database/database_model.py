from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

base = declarative_base()

class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    phone = Column(String(10))

class Passwords(base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key = True, index=True)
    title = Column(String(100))
    user = Column(Integer)
    password = Column(String(100))
    last_updated = Column(Date)