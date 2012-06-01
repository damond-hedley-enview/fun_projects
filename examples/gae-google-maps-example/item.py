from google.appengine.ext import db

class Item(db.Model):
  title = db.StringProperty()
  user = db.StringProperty()
  price = db.StringProperty()
  desc = db.StringProperty()
  location = db.GeoPtProperty()

def insert_def_items():
    items = db.GqlQuery( "SELECT * FROM Item").fetch(1)
    if len(items) == 0 :
        itemarray= []
        itemarray.append(Item( title = 'iphone1', user = 'jimmy', price = '1000', desc = 'sixty percent new', location = db.GeoPt(31.199, 121.587)))
        itemarray.append(Item( title = 'iphone2', user = 'bob', price = '1500', desc = 'sixty-five percent new', location = db.GeoPt(31.297, 121.587)))
        itemarray.append(Item( title = 'iphone3', user = 'john', price = '2000', desc = 'seventy percent new', location = db.GeoPt(31.096, 121.587)))
        itemarray.append(Item( title = 'iphone4', user = 'spiderman', price = '3000', desc = 'eigty percent new', location = db.GeoPt(31.199, 121.487)))
        itemarray.append(Item( title = 'iphone5', user = 'ironman', price = '5000', desc = 'ninty percent new', location = db.GeoPt(31.297, 121.687)))
        itemarray.append(Item( title = 'iphone6', user = 'superman', price = '10000', desc = 'comming soon', location = db.GeoPt(31.096, 121.787)))
        db.put(itemarray)