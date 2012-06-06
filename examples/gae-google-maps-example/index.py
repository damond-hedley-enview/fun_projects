import bottle
from bottle import run, route, default_app
from bottle import static_file, response, template, request
from bottle import jinja2_view as view
from google.appengine.ext import db

from geo import geotypes

import item
from item import Item
item.insert_def_items()

@route('/')
@view('static/views/index.html')
def main_page():
    return {}

@route('/item/latest')
def latest_items():
    response.content_type = 'application/json'
    items = db.GqlQuery( "SELECT * FROM Item").fetch(10)
    return results_dump(items)


#http://localhost:8082/item/nearby?type=center&lat=31.199&lon=121.587&maxresults=10&maxdistance=10000
#http://localhost:8082/item/nearby?type=box&north=33.297&east=122.687&south=30.000&west=121.200&maxresults=100
@route('/item/nearby')
def nearby_items():
    response.content_type = 'application/json'
    
    if (nearby_param_validate(request) == False):
        return {'status':'error-query-paras'}
    
    try:
        if (request.query.type == 'box'):
            bounds = geotypes.Box(float(request.query.north), float(request.query.east),
                                  float(request.query.south), float(request.query.west))
        elif (request.query.type == 'center'):
            center = geotypes.Point(float(request.query.lat), float(request.query.lon))
    except:
        return {'status':'invalid-query-paras'}
    
    max_results = int(request.query.maxresults or '100')
    max_distance = float(request.query.maxdistance or '80000')  # 80 km ~ 50 mi
    
    try:
        base_query = Item.all()
        if (request.query.type == 'box'):
            results = Item.bounding_box_fetch(base_query, bounds, max_results = max_results)
        elif (request.query.type == 'center'):
            results = Item.proximity_fetch(base_query, center, max_results = max_results, max_distance=max_distance)
        return results_dump(results)
    except:
      return {'status':'error-database-query'}

def results_dump(items):
    if len(items) == 0 :
        return {'status':'non-results'}
    
    result_obj = []
    for item in items :
        item_dict = {}
        item_dict['title'] = item.title
        item_dict['lat'] = item.location.lat
        item_dict['lon'] = item.location.lon
        result_obj.append(item_dict)
    return {'status':'success', 'num': len(items), 'results' : result_obj}

def nearby_param_validate(request):
    if (request.query.type):
        if (request.query.type == 'box'):
            if (request.query.north and request.query.east and request.query.south and request.query.west):
                return True
        elif (request.query.type == 'center'):
            if (request.query.lat and request.query.lon):
                return True
    return False


@route('/static/css/:filename')
def server_static(filename):
    return static_file(filename, root='static/css')

@route('/static/js/:filename')
def server_static(filename):
    return static_file(filename, root='static/js')

@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root='static')

@route('/static/img/:filename')
def server_static(filename):
    return static_file(filename, root='static/img')




bottle.debug(True)
app = default_app()


        
