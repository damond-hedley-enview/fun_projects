import bottle
from bottle import route, run, request, response, debug
import json
 
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'test'
DATABASE_PORT = 27017
 
import pymongo
from pymongo import Connection
connection = Connection(DATABASE_HOST, DATABASE_PORT)
db = connection[DATABASE_NAME]
dbtable = db.mongo_test

if dbtable.find().count() < 1 :
    dbtable.insert({'title' : 'iphone1', 'lat' : '1.1', 'lng' : '1.2', 'des' : '60 percent new' })
    dbtable.insert({'title' : 'iphone2', 'lat' : '1.2', 'lng' : '1.3', 'des' : '70 percent new' })
    dbtable.insert({'title' : 'iphone3', 'lat' : '1.3', 'lng' : '1.4', 'des' : '80 percent new' })
    dbtable.insert({'title' : 'iphone4', 'lat' : '1.4', 'lng' : '1.5', 'des' : '90 percent new' })
    dbtable.insert({'title' : 'iphone4s', 'lat' : '1.5', 'lng' : '1.6', 'des' : '95 percent new' })

@route('/item', method='POST')
def insert_items():
    data = request.json
    item = {'title':data['title'], 'lat' : data['lat'], 'lng' : data['lng'], 'des' : data['des'] }
    dbtable.insert(item)
    response.content_type = 'application/json'
    return {'error' : 0}

@route('/item', method='GET')
def get_items():
    q = request.GET.get('title')
    items = dbtable.find({'title' : q})
    response.content_type = 'application/json'
    if items.count() >= 1 :
        ret = {'error' : 0, 'items' : []}
        for it in items :
            ret['items'].append({'title':it['title'], 'lat' : it['lat'], 'lng' : it['lng'], 'des' : it['des'] })
        return ret
    else:
        return {'error' : 1}

debug(True)
run(host='localhost', port=8081)
