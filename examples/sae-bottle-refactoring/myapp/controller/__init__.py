
import bottle
from bottle import route, run, debug, Bottle
from bottle import static_file, response, template, request
from bottle import HTTPError
from bottle import jinja2_view as view

from db import session, sqlalchemy_plugin
from db import User, Item

app = Bottle()
app.install(sqlalchemy_plugin)

import user, item

app.mount('/user', user.app)
app.mount('/item', item.app)

@app.route('/')
@view('static/view/index.html')
def main_page():
    return {}
    
@app.route('/submit')
@view('static/view/submit.html')
def submit_item():
    return {}