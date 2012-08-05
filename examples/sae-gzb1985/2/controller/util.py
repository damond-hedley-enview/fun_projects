
from db import dbsession
from db import User, Item
from hashlib import md5
import string

def encrypt( string ):
    hash_md5 = md5(string)
    md5_data = hash_md5.hexdigest()
    return md5_data
  
def checkUser(username, password):
    user = dbsession.query( User ).filter_by( name = username ).first()
    if user:
        password_db = user.password
        password_encrypt = encrypt( username + password )
        if password_encrypt == password_db:
            return True
    return False

def isUserExsit(username):
    user = dbsession.query( User ).filter_by( name = username ).first()
    if user:
        return True
    return False

