
import os
from db import dbsession
from dbclass import Item, User

def populate_db():
    users = dbsession.query(User).all()
    if not users:
        jimmy = User(name='jimmy', password='12345')
        jimmy.itemlist.append(Item(title='iphone1', price='1000', desc='sixty percent new', location='POINT(%s %s)' %('31.199', '121.587')))
        jimmy.itemlist.append(Item(title='iphone2', price='1500', desc='sixty-five percent new', location='POINT(%s %s)' %('31.299', '121.587')))
        jimmy.itemlist.append(Item(title='iphone3', price='2000', desc='seventy percent new', location='POINT(%s %s)' %('31.099', '121.587')))
        jimmy.itemlist.append(Item(title='iphone4', price='3000', desc='eighty percent new', location='POINT(%s %s)' %('31.199', '121.487')))
        jimmy.itemlist.append(Item(title='iphone4s', price='4000', desc='ninty percent new', location='POINT(%s %s)' %('31.099', '121.787')))
        jimmy.itemlist.append(Item(title='iphone5', price='9999', desc='comming soon...', location='POINT(%s %s)' %('31.199', '121.587')))
        dbsession.add(jimmy)
        
        lisa = User(name='lisa',  password='123456')
        lisa.itemlist.append(Item(title='iphone6', price='99999', desc='future...', location='POINT(%s %s)' %('31.299', '121.387')))
        lisa.itemlist.append(Item(title='iphone7', price='999999', desc='future...', location='POINT(%s %s)' %('31.199', '121.387')))
        dbsession.add(lisa)
        
        dbsession.add(User(name='bob',   password='1234567'))
        dbsession.add(User(name='john',  password='12345678'))
        dbsession.commit()