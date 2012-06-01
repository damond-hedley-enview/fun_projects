import bottle
from bottle import run, route, default_app
from bottle import static_file, response, template, request
from bottle import jinja2_view as view
from google.appengine.ext import db

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
    items = db.GqlQuery( "SELECT * FROM Item").fetch(5)
    result_obj = []
    if len(items) == 0 :
        return {'status':'error'}
    else:
        for item in items :
            item_dict = {}
            item_dict['title'] = item.title
            item_dict['lat'] = item.location.lat
            item_dict['lon'] = item.location.lon
            result_obj.append(item_dict)
    return {'status':'success', 'results' : result_obj}


@route('/static/css/:filename')
def server_static(filename):
    return static_file(filename, root='static/css')

@route('/static/js/:filename')
def server_static(filename):
    return static_file(filename, root='static/js')

@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root='static')


bottle.debug(True)
app = default_app()


        
