import os
import bottle
from bottle import route, Bottle
from bottle import static_file, response, template, request
from bottle import HTTPError

from db import dbsession
from db import Item, User
from db import search_nearby_box
from db import deployed_on_sae

app = Bottle()

#http://localhost:8080/item/add?title=iphone7&price=1000000&desc=future......&lat=32.099&lng=121.287&username=jimmy
@app.route('/add', method='GET')
@app.route('/add', method='POST')
def add_item():
    title = request.GET.get('title')
    price = request.GET.get('price')
    desc = request.GET.get('description')
    latlng = request.GET.get('latlng')
    [lat, lng] = latlng.split(',')
    username = request.GET.get('username')

    user = dbsession.query(User).filter_by(name=username).first()
    if not user:
        #return HTTPError(404, 'User not found.')
        return {'status' : 'error'}
    
    item = Item(title=title, price=price, desc=desc, location='POINT(%s %s)' %(lat, lng))
    user.itemlist.append(item)
    dbsession.commit()
    #return "item %s added!" % title
    return {'status' : 'ok'}
    
@app.route('/latest')
def latest_items():
    response.content_type = 'application/json'
    items = dbsession.query(Item).limit(10).all()
    return item_dump(items)
    
@app.route('/:title')
def get_item(title):
    item = dbsession.query(Item).filter_by(title=title).first()
    if item:
        return "<li>%s by %s</li>" % (item.title, item.user.name)
    return HTTPError(404, 'Item not found.')

#http://gzb1985.sinaapp.com/item/nearby?type=box&north=33.297&east=122.687&south=30.000&west=121.200&maxresults=100
@app.route('/nearby')
def nearby_items():
    response.content_type = 'application/json'
    if (nearby_param_validate(request) == False):
        return {'status':'error-query-params'}

    north = request.GET.get('north')
    south = request.GET.get('south')
    west = request.GET.get('west')
    east = request.GET.get('east')
    max_results = int(request.GET.get('maxresults') or '20')
    
    items = search_nearby_box(north, east, south, west, max_results)
    if items:
        return item_dump(items)
    return {'status':'error-database-query'}
     
def item_dump(items):
    if len(items) == 0 :
        return {'status':'non-results'}
    else:
        results = [item.json() for item in items]
    if not deployed_on_sae:
        for item in results:
            item['latlng'] = {'lat': '31.196784', 'lng' : '121.586530'}
    return {'status':'success', 'num': len(items), 'results' : results}

def nearby_param_validate(request):
    if (request.GET.get('type')):
        if (request.GET.get('type') == 'box'):
            if (request.GET.get('north') and request.GET.get('east') and request.GET.get('south') and request.GET.get('west')):
                return True
        elif (request.GET.get('type') == 'center'):
            if (request.GET.get('lat') and request.GET.get('lng')):
                return True
    return False