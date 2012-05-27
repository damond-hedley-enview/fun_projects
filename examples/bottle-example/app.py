from bottle import route, run, debug
from bottle import static_file, response, template, request
from bottle import jinja2_view as view

@route('/')
@view('views/index.html')
def homepage():
    return {'UserName' : 'Stranger'}

@route('/hello/:name')
@view('views/index.html')
def greet(name):
    #return 'Hello %s, how are you?' % name
    return {'UserName' : name}

@route('/login')
def login_form():
    return '''<form method="POST">
                <input name="name"     type="text" />
                <input name="password" type="password" />
              </form>'''

@route('/login', method='POST')
def login_submit():
    name     = request.forms.get('name')
    password = request.forms.get('password')
    return "<p>Your login name: %s</p>" % name

@route('/static/img/:filename')
def server_static(filename):
    return static_file(filename, root='static/img')

@route('/static/css/:filename')
def server_static(filename):
    return static_file(filename, root='static/css')

@route('/static/js/:filename')
def server_static(filename):
    return static_file(filename, root='static/js')

@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root='static')


class Item:
    def __init__(self, title, lat, lon):
        self.title = title
        self.lat = lat
        self.lon = lon

Items = []
Items.append(Item('t1', '1', '1'))
Items.append(Item('t2', '2', '2'))
Items.append(Item('t3', '3', '3'))

@route('/item/latest')
@view('views/item_latest.xml')
def item_latest():
    response.content_type = 'text/xml'
    return {'totleItems':len(Items), 'items':Items}

@route('/item')
def item_detail():
    lat = request.query['lat']
    lon = request.query['lon']
    response.content_type = 'text/xml'
    return template('item_detail', name='jimmy', lat=lat, lon=lon)


debug(True)
run(host='localhost', port=8080)
