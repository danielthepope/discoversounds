import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


database = os.getenv('DATABASE') or 'sqlite:///radio-sample.db'
print('DATABASE', database)
engine = create_engine(database)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from discoversounds import models
    Base.metadata.create_all(bind=engine)
