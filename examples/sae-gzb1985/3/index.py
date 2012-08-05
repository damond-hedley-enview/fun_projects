#!/usr/bin/python
#-*- coding:utf8 -*-

from bottle import request, response,redirect,template
from db import session,UserInfo
from bottle import jinja2_view as view
import bottle
from weibo import APIClient
from hashlib import md5

import simplejson as json

import urllib2
import re
import sae.kvdb

qq_appid = '100285829'
qq_secret = 'b2026351acba2742dec6087b4b51f051'

redirect_url_weibo = "http://gzb1985.sinaapp.com/weibo"
redirect_url_qq = "http://gzb1985.sinaapp.com/qq"

authorization_url_qq = 'https://graph.qq.com/oauth2.0/authorize'
access_token_url_qq = 'https://graph.qq.com/oauth2.0/token'
openid_url_qq = 'https://graph.qq.com/oauth2.0/me'

weibo_appid = '2023070208'
weibo_app_secret='abb0afabbd3b82348971b1c6ad891c2c'

def encrypt( string ):
  hash_md5 = md5(string)
  md5_data = hash_md5.hexdigest()
  return md5_data


def checkUser(user, password):
  userinfo = session.query( UserInfo ).filter_by( username = user ).first()

  if not userinfo:
    return False

  password_db = userinfo.password
  password_encrypt = encrypt( user + password )
  
  if password_encrypt[0:20] == password_db:
    return True
  else:
    return False


class just(object):
  def __init__(self, arg='w'):
    self.arg = arg
  
  def show(self):
    return 'ok'                    
        
class user_action(object):
  """docstring for user_action"""
  def __init__(self, arg='w'):
    self.arg = arg
    return '%s' %arg
    
  @classmethod
  def index(cls):
    beaker_session = request.environ['beaker.session']
    if 'cookies_value' in beaker_session:
      username = beaker_session['cookies_value']
      return { 'username': username }
    return {}
  
  @classmethod
  def signin(cls):
    name = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    
    if len(name)==0:
      return "username is null"

    userinfo = session.query( UserInfo ).filter_by( username = name ).first()
    if userinfo:
      return "user has already exist!"
      
    password_encrypt = encrypt( name + password )
    userinfo = UserInfo( username=name, password=password_encrypt, email=email )
    session.add(userinfo)
    session.commit()
    return redirect( '/' ) 
    
  @classmethod
  @view('static/view/index.html')
  def login(cls):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    beaker_session = request.environ['beaker.session']
    if checkUser( username, password ) == True:
      beaker_session['cookies_value'] = username

      if request.get_cookie('cookies_value_client', username ):

        if username == request.get_cookie('cookies_value_client', username ):
          beaker_session.save()
          response.set_cookie('cookies_value_client', username)
          return { 'username': username}
        else:
          beaker_session.save()
          response.set_cookie( 'cookies_value_client', username )
          return { 'username': username}
          #return template( 'static/view/index.html', username=username)
      else:
        beaker_session.save()
        response.set_cookie('cookies_value_client', username)
        return { 'username': username}
        #return template('static/view/index.html', username=username)
    else:
      beaker_session = request.environ['beaker.session']
      beaker_session.delete()
      return 'no user'

  @classmethod
  def logout(cls):
    beaker_session = request.environ['beaker.session']

    if 'cookies_value' in beaker_session:
      value = beaker_session['cookies_value']
      response.delete_cookie('cookies_value_client')
      beaker_session.delete()
      redirect('/')
    else:
      return {}

  @classmethod
  def index_beaker(cls):
    count = int( request.cookies.get('counter', '0') )
    count = count + 1
    response.set_cookie( 'counter', str(count) )
    return 'You visited for %s times' %count
    #return 'Hello world! You have refrush for %s times' %str(refrush_times)    


  @classmethod
  def index_beaker_server(cls):
    return  {}
#    mc = pylibmc.Client()
#    mc.set("foo", "bar")
#    value = mc.get("foo")
#    return '%s ' %value


  @classmethod
  def login_to_qq(cls):
    url = authorization_url_qq + "?response_type=code&client_id="+qq_appid+"&redirect_uri="+redirect_url_qq
    return bottle.redirect(url)
  
  @classmethod
  def login_to_weibo(cls):
    client = APIClient(app_key=weibo_appid, app_secret=weibo_app_secret, redirect_uri=redirect_url_weibo)
    url = client.get_authorize_url()
    bottle.redirect(url)
    
  @classmethod
  def qq(cls):
    code = bottle.request.GET.get('code')
    url = access_token_url_qq + "?grant_type=authorization_code&client_id="+qq_appid+"&client_secret="+qq_secret+\
              "&code="+code+"&state=test&redirect_uri="+redirect_url_qq
  
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
    
    url = 'https://graph.qq.com/user/get_info?access_token='+access_token+'&oauth_consumer_key='+oauth_consumer_key+'&openid='\
           +openid_qq
  
    f = urllib2.urlopen(url)
    s = f.read()
    dict_s = eval(s)
    
    return s
    
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
    
    
  @classmethod
  @view('static/view/test.tpl')
  def weibo(cls):
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

    else:
      return 'no'
    

  
  
session_opts = {
  'session.type': 'cookie',
  'session.expires': 300,
  'session.validate_key': '1234',
}

#
#session_opts = {
#  'session.type': 'ext:database',
#  'session.expires': 300,
#  'session.url': 'sqlite:///./test.db',
#  'session.data_dir': 'sqlite:///./test.db',
#}


#session_opts = {
#  'session.type': 'cookie',
#  'session.expires': 100,
#  'session.validate_key': 1234,
#  'session.cookie_domain': '/',
#  'session.path' = '/login/login',
#  'session.url': '127.0.0.1:11211',
#}
