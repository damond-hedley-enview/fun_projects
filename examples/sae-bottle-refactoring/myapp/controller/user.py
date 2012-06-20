
import bottle
from bottle import route, Bottle
from bottle import static_file, response, template, request
from bottle import HTTPError

from db import session, sqlalchemy_plugin
from db import User, Item

app = Bottle()
app.install(sqlalchemy_plugin)

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

@app.route('/list')
def users(db):
    users = db.query(User)
    if users:
    	result = "".join(["<li>%s</li>" % user.name for user in users])
    	return "<ul>%s</ul>" % result
    return HTTPError(404, 'User not found.')
    
@app.route('/:name')
def user_name(name, db):
    user = db.query(User).filter_by(name=name).first()
    if user:
        return "<li>%s found</li>" % (user.name)
    return HTTPError(404, 'User not found.')
