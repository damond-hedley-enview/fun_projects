import os
import bottle
from bottle import Bottle

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, column_property

app = Bottle()

if 'SERVER_SOFTWARE' in os.environ:
    import sae.const
    import sae.storage
    from sae.const import MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB

if 'SERVER_SOFTWARE' in os.environ:
    engine = create_engine('mysql://%s:%s@%s:%s/app_gzb1985?charset=utf8' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT),
                            encoding='utf8', echo=False, pool_recycle=4)
else:
    engine = create_engine('sqlite:///./test.db?check_same_thread=False', echo=True)

metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)
Session = sessionmaker(bind=engine)
session = Session()


#from bottle.ext import sqlalchemy
#sqlalchemy_plugin = sqlalchemy.Plugin(
#    engine, # SQLAlchemy engine created with create_engine function.
#    Base.metadata, # SQLAlchemy metadata, required only if create=True.
#    keyword='db', # Keyword used to inject session database in a route (default 'db').
#    create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
#    commit=True, # If it is true, plugin commit changes after route is executed (default True).
#    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
#)

