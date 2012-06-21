import bottle
from bottle import route, Bottle
from bottle import static_file, response, template, request
from bottle import HTTPError

from db import session#, sqlalchemy_plugin
from db import Item, User

app = Bottle()
#app.install(sqlalchemy_plugin)

#http://gzb1985.sinaapp.com/additem?title=iphone1&price=1000&desc=sixty percent new&lat=31.199&lng=121.587
#http://gzb1985.sinaapp.com/additem?title=iphone2&price=1500&desc=sixty-five percent new&lat=31.299&lng=121.587
#http://gzb1985.sinaapp.com/additem?title=iphone3&price=2000&desc=seventy percent new&lat=31.096&lng=121.587
#http://gzb1985.sinaapp.com/additem?title=iphone4&price=3000&desc=eighty percent new&lat=31.199&lng=121.487
#http://gzb1985.sinaapp.com/additem?title=iphone4s&price=4000&desc=ninty percent new&lat=31.299&lng=121.687
#http://gzb1985.sinaapp.com/additem?title=iphone5&price=10000&desc=comming soon&lat=31.096&lng=121.787
#http://gzb1985.sinaapp.com/additem?title=iphone6&price=100000&desc=future...&lat=30.096&lng=121.287
#http://gzb1985.sinaapp.com/additem?title=iphone7&price=1000000&desc=future......&lat=32.099&lng=121.287
@app.route('/add')
def add_item():
    title = request.GET.get('title')
    price = request.GET.get('price')
    desc = request.GET.get('desc')
    lng = request.GET.get('lng')
    lat = request.GET.get('lat')
    
    item = Item(title=title, price=price, desc=desc)
    user = session.query(User).filter_by(name='jimmy1').first()
    user.itemlist.append(item)
    session.commit()
    return "user %s added!" % title
    
@app.route('/latest')
def latest_items():
    response.content_type = 'application/json'
    items = session.query(Item).all()
    return results_dump(items)
    
@app.route('/:title')
def get_item(title):
    item = session.query(Item).filter_by(title=title).first()
    if item:
        return "<li>%s at: %s, %s</li>" % (item.title, session.scalar(item.location.x), session.scalar(item.location.y))
    return HTTPError(404, 'User not found.')

#http://gzb1985.sinaapp.com/item/nearby?type=box&north=33.297&east=122.687&south=30.000&west=121.200&maxresults=100
@app.route('/nearby')
def nearby_items():
    response.content_type = 'application/json'
    
    if (nearby_param_validate(request) == False):
        return {'status':'error-query-paras'}
    
    north = request.GET.get('north')
    south = request.GET.get('south')
    west = request.GET.get('west')
    east = request.GET.get('east')
    #box = "POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))" % (north, east, south, east, south, west, north, west, north, east)
    #max_results = int(request.GET.get('maxresults') or '100')
    #items = session.query(Item).filter(Item.location.within(box)).limit(max_results)
    items1 = items.all()
    if items1:
        return results_dump(items1)
    return {'status':'error-database-query'}
     
def results_dump(items):
    if len(items) == 0 :
        return {'status':'non-results'}
    
    result_obj = []
    for item in items :
        item_dict = {}
        item_dict['title'] = item.title
        item_dict['user'] = item.user_id
        item_dict['price'] = item.price
        item_dict['desc'] = item.desc
        item_dict['latlng'] = {}
        #item_dict['latlng']['lat'] = session.scalar(item.location.x)
        #item_dict['latlng']['lng'] = session.scalar(item.location.y)
        result_obj.append(item_dict)
    return {'status':'success', 'num': len(items), 'results' : result_obj}

def nearby_param_validate(request):
    if (request.GET.get('type')):
        if (request.GET.get('type') == 'box'):
            if (request.GET.get('north') and request.GET.get('east') and request.GET.get('south') and request.GET.get('west')):
                return True
        elif (request.GET.get('type') == 'center'):
            if (request.GET.get('lat') and request.GET.get('lng')):
                return True
    return False