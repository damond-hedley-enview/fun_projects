
import os
from depend import deployed_on_sae

from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from db import Base, dbsession

if deployed_on_sae:
    from geoalchemy import (Geometry, Point, LineString, Polygon, GeometryColumn, GeometryDDL, WKTSpatialElement)
else:
    #stubs for local
    from sqlalchemy import Column as GeometryColumn
    from sqlalchemy import String as Point


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(80))
    email = Column(String(50))
    type = Column(String(10), nullable=False)#normal, weibo

    #user-to-item: one-to-many
    itemlist = relationship("Item", order_by="Item.id", backref="user")
    weibo_id = Column(Integer, ForeignKey('weibo.id'))
    weibo = relationship("Weibo", backref=backref("user", uselist=False))
    
    def __init__(self, name, password='', email='', type='normal'):
        self.name = name
        self.password = password
        self.email = email
        self.type = type

    def json(self):
        return {'name' : self.name, 'email' : self.email, 'type' : self.type}

class Weibo(Base):
    __tablename__ = 'weibo'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    access_token = Column(String(50), nullable=False)
    expires_in = Column(Integer, nullable=False)
    profile_image_url = Column(String(100), nullable=False)
    
    def __init__(self, uid, name, access_token, expires_in, profile_image_url):
        self.uid = uid
        self.name = name
        self.access_token = access_token
        self.expires_in = expires_in
        self.profile_image_url = profile_image_url

    def json(self):
        return {'uid' : self.uid, 'name' : self.name, 'profile_image_url' : self.profile_image_url}

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    price = Column(String(20), nullable=False)
    desc = Column(String(150), nullable=False)
    location = GeometryColumn(Point(2), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    
    def __init__(self, title, price, desc, location=''):
        self.title = title
        self.price = price
        self.desc = desc
        self.location = location

    def json(self): 
        item_json = {'title' : self.title, 'price' : self.price, 'desc' : self.desc, 'user' : self.user.json()}
        if deployed_on_sae:
            item_json['latlng'] = {'lat' : dbsession.scalar(self.location.x), 'lng' : dbsession.scalar(self.location.y)}
        return item_json

if deployed_on_sae:
    GeometryDDL(Item.__table__)

#comment drop_all() after first use
#Base.metadata.drop_all()
Base.metadata.create_all()


