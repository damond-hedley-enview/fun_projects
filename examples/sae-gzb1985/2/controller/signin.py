#!/usr/bin/python
#-*- coding:utf8 -*-
import bottle
from bottle import route, Bottle
from bottle import static_file, response, template, request
from bottle import HTTPError
from bottle import jinja2_view as view

from db import dbsession
from db import User, Item
from util import encrypt

app = Bottle()


@app.route('/', method='GET')
@view('static/view/signin.html')
def signin_page():
  return {}  

@app.route('/', method='POST')
@view('static/view/index.html')
def signin():
  username = request.POST.get('username')
  password = request.POST.get('password')
  email = request.POST.get('email')
  if not username or not password or not email : 
    return HTTPError(404, 'no data.')

  password_encrypt = encrypt( username + password )
  user = User(name=username, password=password_encrypt, email=email)
  dbsession.add(user)
  dbsession.commit()
  session = request.environ['beaker.session']
  session['username'] = username
  session.save()
  return {'username' : username}
