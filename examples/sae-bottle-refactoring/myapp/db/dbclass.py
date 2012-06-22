
from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from db import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(20), nullable=False)

    #user-to-item: one-to-many
    itemlist = relationship("Item", order_by="Item.id", backref="user")
    
    def __init__(self, name, password):
        self.name = name
        self.password = password

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    price = Column(String(20), nullable=False)
    desc = Column(String(150), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    
    def __init__(self, title, price, desc):
        self.title = title
        self.price = price
        self.desc = desc

#Base.metadata.drop_all()
Base.metadata.create_all()