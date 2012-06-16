
import os
import sae
import bottle
from bottle import route, run, debug, Bottle
from bottle import static_file, response, template, request
from bottle import HTTPError
from bottle import jinja2_view as view

from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, column_property
from geoalchemy import (Geometry, Point, LineString, Polygon, GeometryColumn, GeometryDDL, WKTSpatialElement)


if 'SERVER_SOFTWARE' in os.environ:
    import sae.const
    import sae.storage
    from sae.const import MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB

if 'SERVER_SOFTWARE' in os.environ:
    engine = create_engine('mysql://%s:%s@%s:%s/app_gzb1985?charset=utf8' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT),
                            encoding='utf8', echo=False, pool_recycle=4)
else:
    engine = create_engine('sqlite:///./test.db', echo=True)
metadata = MetaData(engine)
session = sessionmaker(bind=engine)()
Base = declarative_base(metadata=metadata)

app = bottle.Bottle()

plugin = sqlalchemy.Plugin(
    engine, # SQLAlchemy engine created with create_engine function.
    Base.metadata, # SQLAlchemy metadata, required only if create=True.
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)
app.install(plugin)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(12), nullable=False)
    location = GeometryColumn(Point(2), nullable=False)
    
    def __init__(self, name, password, location):
        self.name = name
        self.password = password
        self.location = location

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    title = Column(String(50), nullable=False)
    price = Column(String(12), nullable=False)
    desc = Column(String(200), nullable=False)
    location = GeometryColumn(Point(2), nullable=False)
    
    def __init__(self, title, price, desc, location):
        self.title = title
        self.price = price
        self.desc = desc
        self.location = location
        

GeometryDDL(User.__table__)
GeometryDDL(Item.__table__)
#metadata.drop_all()
metadata.create_all()


@app.route('/')
@view('static/view/index.html')
def main_page():
    return {}
    
@app.route('/submit')
@view('static/view/submit.html')
def submit_item():
    return {}

#http://localhost:8080/add?name=lisa&password=123&lng=1.23&lat=2.23
#http://localhost:8080/add?name=jimmy&password=234&lng=2.23&lat=3.23
@app.route('/add')
def add(db):
    name = request.GET.get('name')
    password = request.GET.get('password')
    lng = request.GET.get('lng')
    lat = request.GET.get('lat')
    
    user = User(name=name, password=password, location='POINT(%s %s)' %(lat, lng))
    session.add(user)
    session.commit()
    return "user %s added!" % name

@app.route('/user')
def user_name(db):
    users = db.query(User)
    if users:
    	result = "".join(["<li>%s</li>" % user.name for user in users])
    	return "<ul>%s</ul>" % result
    return HTTPError(404, 'User not found.')
    
@app.route('/user/:name')
def user_name(name, db):
    user = db.query(User).filter_by(name=name).first()
    if user:
        return "<li>%s at: %s, %s</li>" % (user.name, session.scalar(user.location.x), session.scalar(user.location.y))
    return HTTPError(404, 'User not found.')


#http://gzb1985.sinaapp.com/additem?title=iphone1&price=1000&desc=sixty percent new&lat=31.199&lng=121.587
#http://gzb1985.sinaapp.com/additem?title=iphone2&price=1500&desc=sixty-five percent new&lat=31.299&lng=121.587
#http://gzb1985.sinaapp.com/additem?title=iphone3&price=2000&desc=seventy percent new&lat=31.096&lng=121.587
#http://gzb1985.sinaapp.com/additem?title=iphone4&price=3000&desc=eighty percent new&lat=31.199&lng=121.487
#http://gzb1985.sinaapp.com/additem?title=iphone4s&price=4000&desc=ninty percent new&lat=31.299&lng=121.687
#http://gzb1985.sinaapp.com/additem?title=iphone5&price=10000&desc=comming soon&lat=31.096&lng=121.787
#http://gzb1985.sinaapp.com/additem?title=iphone6&price=100000&desc=future...&lat=30.096&lng=121.287
#http://gzb1985.sinaapp.com/additem?title=iphone7&price=1000000&desc=future......&lat=32.099&lng=121.287
@app.route('/additem')
def add_item(db):
    title = request.GET.get('title')
    price = request.GET.get('price')
    desc = request.GET.get('desc')
    lng = request.GET.get('lng')
    lat = request.GET.get('lat')
    
    item = Item(title=title, price=price, desc=desc, location='POINT(%s %s)' %(lat, lng))
    session.add(item)
    session.commit()
    return "user %s added!" % title
    
@app.route('/item/latest')
def latest_items(db):
    response.content_type = 'application/json'
    items = db.query(Item).all()
    return results_dump(items)
    
@app.route('/item/:title')
def get_item(title, db):
    item = db.query(Item).filter_by(title=title).first()
    if item:
        return "<li>%s at: %s, %s</li>" % (item.title, session.scalar(item.location.x), session.scalar(item.location.y))
    return HTTPError(404, 'User not found.')

#http://gzb1985.sinaapp.com/item/nearby?type=box&north=33.297&east=122.687&south=30.000&west=121.200&maxresults=100
@app.route('/item/nearby')
def nearby_items(db):
    response.content_type = 'application/json'
    
    if (nearby_param_validate(request) == False):
        return {'status':'error-query-paras'}
    
    north = request.GET.get('north')
    south = request.GET.get('south')
    west = request.GET.get('west')
    east = request.GET.get('east')
    box = "POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))" % (north, east, south, east, south, west, north, west, north, east)
    max_results = int(request.GET.get('maxresults') or '100')
    items = db.query(Item).filter(Item.location.within(box)).limit(max_results)
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
        #item_dict['user'] = item.user
        item_dict['price'] = item.price
        item_dict['desc'] = item.desc
        item_dict['latlng'] = {}
        item_dict['latlng']['lat'] = session.scalar(item.location.x)
        item_dict['latlng']['lng'] = session.scalar(item.location.y)
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
    
    
debug(True)
application = sae.create_wsgi_app(app)