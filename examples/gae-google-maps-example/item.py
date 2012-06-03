from google.appengine.ext import db
from geo.geomodel import GeoModel

class Item(GeoModel):
  title = db.StringProperty()
  user = db.StringProperty()
  price = db.StringProperty()
  desc = db.StringProperty()
  
  @staticmethod
  def public_attributes():
    """Returns a set of simple attributes on public school entities."""
    return [
      'title', 'user', 'price', 'desc', 'state'
      ]

  def _get_latitude(self):
    return self.location.lat if self.location else None

  def _set_latitude(self, lat):
    if not self.location:
      self.location = db.GeoPt()
    self.location.lat = lat

  latitude = property(_get_latitude, _set_latitude)

  def _get_longitude(self):
    return self.location.lon if self.location else None

  def _set_longitude(self, lon):
    if not self.location:
      self.location = db.GeoPt()
    self.location.lon = lon

  longitude = property(_get_longitude, _set_longitude)

def insert_def_items():
    items = db.GqlQuery( "SELECT * FROM Item").fetch(1)
    if len(items) == 0 :
        itemarray= []
        item1 = Item( title = 'iphone1', user = 'jimmy', price = '1000', desc = 'sixty percent new', location = db.GeoPt(31.199, 121.587))
        item1.update_location()
        itemarray.append(item1)

        item2 = Item( title = 'iphone2', user = 'bob', price = '1500', desc = 'sixty-five percent new', location = db.GeoPt(31.297, 121.587))
        item2.update_location()
        itemarray.append(item2)

        item3 = Item( title = 'iphone3', user = 'john', price = '2000', desc = 'seventy percent new', location = db.GeoPt(31.096, 121.587))
        item3.update_location()
        itemarray.append(item3)

        item4 = Item( title = 'iphone4', user = 'spiderman', price = '3000', desc = 'eigty percent new', location = db.GeoPt(31.199, 121.487))
        item4.update_location()
        itemarray.append(item4)

        item5 = Item( title = 'iphone5', user = 'ironman', price = '5000', desc = 'ninty percent new', location = db.GeoPt(31.297, 121.687))
        item5.update_location()
        itemarray.append(item5)

        item6 = Item( title = 'iphone6', user = 'superman', price = '10000', desc = 'comming soon', location = db.GeoPt(31.096, 121.787))
        item6.update_location()
        itemarray.append(item6)

        item7 = Item( title = 'iphone7', user = 'loki', price = '100000', desc = 'comming soon', location = db.GeoPt(30.096, 121.287))
        item7.update_location()
        itemarray.append(item7)

        item8 = Item( title = 'iphone8', user = 'thor', price = '1000000', desc = 'comming soon', location = db.GeoPt(32.096, 121.287))
        item8.update_location()
        itemarray.append(item8)
        
        db.put(itemarray)
