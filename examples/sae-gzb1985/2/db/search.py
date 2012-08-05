import os
from depend import deployed_on_sae

from db import dbsession
from dbclass import Item, User

if deployed_on_sae:
    def search_nearby_box(north, east, south, west, max_results=10):
        box = "POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))" % (north, east, south, east, south, west, north, west, north, east)
        items = dbsession.query(Item).filter(Item.location.within(box)).limit(max_results).all()
        return items
else:
    def search_nearby_box(north, east, south, west, max_results=10):
        items = dbsession.query(Item).limit(max_results).all()
        return items