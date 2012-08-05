
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean

import sae.const
import sae.storage
from sae.const import MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mysql://%s:%s@%s:%s/app_gzb1985?charset=utf8' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT),
                            encoding='utf8', echo=False, pool_recycle=5)
                            


metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)
Session = sessionmaker(bind=engine)
session = Session()


class UserInfo(Base):
  __tablename__ = 'userinfo'
  id = Column( Integer, primary_key = True )
  username = Column( String(50), nullable=False)
  password = Column( String(20), nullable=False)
  email = Column(String(50), nullable=False)

  def __init__( self, username, password, email="example@gmail.com"):
    self.username = username
    self.password = password
    self.email = email

#Base.metadata.drop_all()
Base.metadata.create_all()

