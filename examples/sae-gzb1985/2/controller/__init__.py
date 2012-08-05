

import bottle
from bottle import route, run, debug, Bottle, default_app
from bottle import static_file, response, template, request, redirect
from bottle import HTTPError
from bottle import jinja2_view as view

from db import dbsession
from db import User, Item
from util import *

app = default_app()
bottle.debug(True)

import user, item, login, signin

app.mount('/user', user.app)
app.mount('/item', item.app)
app.mount('/login', login.app)
app.mount('/signin', signin.app)



@app.route('/')
@view('static/view/index.html')
def main_page():
    isLogged, username = login.session_login(request)
    if isLogged == True:
    	return {'username' : username}
    return {}

@app.route('/browser')
@view('static/view/browser.html')
def browser_page():
    return {}
    
@app.route('/submit')
@view('static/view/submit.html')
def submit_item():
    return {}

@app.route('/logout')
def logout():
    login.session_logout(request)
    return redirect('/')



from beaker.middleware import SessionMiddleware
session_opts = {
  'session.type': 'cookie',
  'session.expires': 300,
  'session.validate_key': '1234',
}
app = SessionMiddleware( app, session_opts )
