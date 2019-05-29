import logging as log
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

log.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=log.DEBUG)

database = os.getenv('DATABASE') or 'sqlite:///radio-sample.db'
log.info('DATABASE %s', database)
engine = create_engine(database)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from discoversounds import models
    Base.metadata.create_all(bind=engine)
