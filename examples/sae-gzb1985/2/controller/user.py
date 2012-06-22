
import bottle
from bottle import route, Bottle
from bottle import static_file, response, template, request
from bottle import HTTPError

from db import session
from db import User, Item

app = Bottle()

#http://localhost:8080/user/add?name=lisa&password=123&lng=1.23&lat=2.23
#http://localhost:8080/user/add?name=jimmy&password=234&lng=2.23&lat=3.23
@app.route('/add')
def add():
    name = request.GET.get('name')
    password = request.GET.get('password')
    lng = request.GET.get('lng')
    lat = request.GET.get('lat')
    user = User(name=name, password=password)
    session.add(user)
    session.commit()
    return 'user %s added!' % (name)

@app.route('/list')
def users():
    users = session.query(User)
    if users:
    	result = "".join(["<li>%s</li>" % user.name for user in users])
    	return "<ul>%s</ul>" % result
    return HTTPError(404, 'User not found.')
    
@app.route('/:name')
def user_name(name):
    user = session.query(User).filter_by(name=name).first()
    if user:
        return "<li>%s found, items count %d</li>" % (user.name, len(user.itemlist))
    return HTTPError(404, 'User not found.')
