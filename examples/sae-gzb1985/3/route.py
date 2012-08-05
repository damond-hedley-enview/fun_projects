
from bottle import Bottle, run, template, debug
from bottle import jinja2_view as view
from beaker.middleware import SessionMiddleware

from index import user_action
from index import session_opts
from weibo import APIClient



debug(True)
app = Bottle()

@app.route('/')  
@app.route('/index')
@view('static/view/index.html')
def index():
  return user_action.index()

#@app.route('/')
@app.route('/index/signin', method='POST')
def index_signin():
  return user_action.signin()

@app.route('/index/login', method='POST')
def index_login():
  return user_action.login()
  
@app.route('/index/logout')
def index_logout():
  return user_action.logout()
  

@app.route('/login_to_qq')
def login_to_qq_view():
  return user_action.login_to_qq()
  
@app.route('/login_to_weibo')
def login_to_weibo_view():
  return user_action.login_to_weibo()
  
@app.route('/qq')
def qq_view():
  return user_action.qq()
  
@app.route('/weibo')
def weibo_view():
  return user_action.weibo()
  
  

app = SessionMiddleware( app, session_opts )
  