
from sqlalchemy import Column, Integer, Sequence, String
from db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(12), nullable=False)
    
    def __init__(self, name, password, location):
        self.name = name
        self.password = password
        self.location = location

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    title = Column(String(50), nullable=False)
    price = Column(String(12), nullable=False)
    desc = Column(String(200), nullable=False)
    
    def __init__(self, title, price, desc, location):
        self.title = title
        self.price = price
        self.desc = desc
        self.location = location