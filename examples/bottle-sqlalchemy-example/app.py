import bottle
from bottle import route, run, debug
from bottle import static_file, response, template, request
from bottle import HTTPError

from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
create_session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    password = Column(String(12))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.name, self.password)

#http://localhost:8080/add?name=lisa&password=123
#http://localhost:8080/add?name=jimmy&password=234
@route('/add')
def add(db):
    name = request.query.name
    password = request.query.password
    user = User(name=name, password=password)
    db.add(user)

@route('/user')
def user_name(db):
    users = db.query(User)
    result = "".join(["<li>%s</li>" % user.name for user in users])
    return "<ul>%s</ul>" % result

@route('/user/:name')
def user_name(name, db):
    user = db.query(User).filter_by(name=name).first()
    if user:
        return "<li>%s</li>" % user.name
    return HTTPError(404, 'Entity not found.')

bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=True))

debug(True)
run(host='localhost', port=8080)
