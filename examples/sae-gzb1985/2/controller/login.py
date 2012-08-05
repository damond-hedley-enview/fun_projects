#!/usr/bin/python
#-*- coding:utf8 -*-
import bottle
from bottle import route, Bottle
from bottle import static_file, response, template, request, redirect
from bottle import HTTPError
from bottle import jinja2_view as view

from db import dbsession
from db import User, Item, Weibo
from util import *

app = Bottle()

import urllib2
import json
import re
from weibo import APIClient

redirect_url_weibo = "http://gzb1985.sinaapp.com/login/weibo"
weibo_appid = '2023070208'
weibo_app_secret='abb0afabbd3b82348971b1c6ad891c2c'

def handle_weibo_oauth():
  code = bottle.request.GET.get('code')
  client = APIClient(app_key=weibo_appid, app_secret=weibo_app_secret, redirect_uri=redirect_url_weibo)
  r = client.request_access_token(code)
  
  access_token = r.access_token
  expires_in = r.expires_in
  client.set_access_token(access_token, expires_in)
  
  url = 'https://api.weibo.com/2/statuses/public_timeline.json' + '?access_token='+access_token
  
  f = urllib2.urlopen(url)
  s = f.read()
  weiboString = json.loads(s)
  
  if 'statuses' in weiboString:
    dictString = weiboString['statuses']
    return {'weiboDict':dictString}
  
  #weibo_user = client.get.users__show(uid=r.uid)
  #user = User(name=weibo_user.screen_name, type='weibo')
  #weibo = Weibo(uid=r.uid, name=weibo_user.screen_name, access_token=r.access_token, 
  #  expires_in = r.expires_in, profile_image_url=weibo_user.profile_image_url)
  #user.weibo = weibo
  #dbsession.add(user)
  #dbsession.commit()
  #session = request.environ['beaker.session']
  #session['username'] = weibo_user.screen_name
  #session.save()
  #return {'username' : weibo_user.screen_name, 'profile_image_url' : weibo_user.profile_image_url}

@app.route('/weibo')
@view('static/view/viewWeibo.tpl')
def weibo():
  return handle_weibo_oauth()

@app.route('/login_to_weibo')
def login_to_weibo():
  client = APIClient(app_key=weibo_appid, app_secret=weibo_app_secret, redirect_uri=redirect_url_weibo)
  url = client.get_authorize_url()
  return redirect(url)


qq_appid = '100285829'
qq_secret = 'b2026351acba2742dec6087b4b51f051'
redirect_url_qq = "http://gzb1985.sinaapp.com/login/qq"
authorization_url_qq = 'https://graph.qq.com/oauth2.0/authorize'
access_token_url_qq = 'https://graph.qq.com/oauth2.0/token'
openid_url_qq = 'https://graph.qq.com/oauth2.0/me'

@app.route('/qq')
def qq():
  code = bottle.request.GET.get('code')
  url = access_token_url_qq + "?grant_type=authorization_code&client_id=" + qq_appid + \
        "&client_secret=" + qq_secret + \
        "&code=" + code + "&state=test&redirect_uri=" + redirect_url_qq

  f = urllib2.urlopen(url)
  s = f.read()
  access_token = s[s.find('=')+1:s.find('&')]
  
  url = openid_url_qq + "?access_token=" + access_token
  f = urllib2.urlopen(url)
  s = f.read()
  s = s[10:-3]
  dict_s = eval(s)
  openid_qq = dict_s['openid']
  oauth_consumer_key = dict_s['client_id']
  
  url = 'https://graph.qq.com/user/get_user_info?access_token=' + access_token + \
        '&oauth_consumer_key='+oauth_consumer_key+'&openid=' + openid_qq

  f = urllib2.urlopen(url)
  s = f.read()
  dict_s = eval(s)
  
  return '''
  <html>
    <body>
      <h1>welcome back %s</h1>
    </body>
    <p>
      do u want to see your photos?
      <a href = "%s"> yes</a>
    </p>
    
  </html>
  '''%(dict_s['nickname'], dict_s['figureurl'])

@app.route('/login_to_qq')
def login_to_qq():
  url = authorization_url_qq + "?response_type=code&client_id=" + qq_appid + \
        "&redirect_uri=" + redirect_url_qq
  return redirect(url)
  

  
@app.route('/', method='GET')
@view('static/view/login.html')
def login_page():
  return {}

@app.route('/', method='POST')
@view('static/view/index.html')
def login():
  username = request.POST.get('username')
  password = request.POST.get('password')
  if not username or not password : 
    return HTTPError(404, 'no data.')
  
  if checkUser( username, password ) == True:
    session = request.environ['beaker.session']
    session['username'] = username
    session.save()
    return {'username' : username}
  return HTTPError(404, 'User not found.')

def session_login(request) :
  session = request.environ['beaker.session']
  if 'username' in session:
    username = session['username']
    if isUserExsit(username) :
      return True, username
  return False, None

def session_logout(request) :
  session = request.environ['beaker.session']
  session.delete()