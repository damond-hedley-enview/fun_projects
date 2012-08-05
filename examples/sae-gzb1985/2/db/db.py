import os
from depend import deployed_on_sae

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, column_property

if deployed_on_sae:
    import sae.const
    import sae.storage
    from sae.const import MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB
    engine = create_engine('mysql://%s:%s@%s:%s/app_gzb1985?charset=utf8' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT),
                            encoding='utf8', echo=False, pool_recycle=5)
else:
	engine = create_engine('sqlite:///./test.db?check_same_thread=False', echo=True)

metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)
Session = sessionmaker(bind=engine)
dbsession = Session()


