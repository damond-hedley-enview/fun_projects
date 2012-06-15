
import sae
import bottle
from bottle import route, run, debug, Bottle
from bottle import static_file, response, template, request
from bottle import HTTPError

from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

LOCAL = True
if not LOCAL:
    import sae.const
    import sae.storage
    from sae.const import MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB

Base = declarative_base()

if LOCAL:
    engine = create_engine('sqlite:///./test.db', echo=True)
else:
    engine = create_engine('mysql://%s:%s@%s:%s/app_gzb1985?charset=utf8' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT),
                            encoding='utf8', echo=False, pool_recycle=5)

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(
    engine, # SQLAlchemy engine created with create_engine function.
    Base.metadata, # SQLAlchemy metadata, required only if create=True.
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)

app.install(plugin)


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

@app.route('/')
def hello():
    return "Hello, world! - Bottle"

#http://localhost:8080/add?name=lisa&password=123
#http://localhost:8080/add?name=jimmy&password=234
@app.route('/add')
def add(db):
    name = request.GET.get('name')
    password = request.GET.get('password')
    user = User(name=name, password=password)
    db.add(user)

@app.route('/user')
def user_name(db):
    users = db.query(User)
    result = "".join(["<li>%s</li>" % user.name for user in users])
    return "<ul>%s</ul>" % result

@app.route('/user/:name')
def user_name(name, db):
    user = db.query(User).filter_by(name=name).first()
    if user:
        return "<li>%s</li>" % user.name
    return HTTPError(404, 'Entity not found.')


debug(True)
application = sae.create_wsgi_app(app)