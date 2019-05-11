from sqlalchemy import (Column, DateTime, Integer, MetaData,
                        PrimaryKeyConstraint, String, Table, Boolean)

from discoversounds.database import Base


class Show(Base):
    __tablename__ = 'shows'
    __table_args__ = {'extend_existing': True}
    vpid = Column(String(30), primary_key=True)
    epid = Column(String(30))
    ipid = Column(String(30))
    sid = Column(String(30), nullable=False)
    title = Column(String(255), nullable=False)
    synopsis = Column(String(1024))
    availability_from = Column(DateTime())
    availability_to = Column(DateTime())


class ShowToArtist(Base):
    __tablename__ = 'show_to_artist'
    __table_args__ = {'extend_existing': True}
    vpid = Column(String(30), primary_key=True)
    artist = Column(String(255), primary_key=True)
    expiry = Column(DateTime())

class Service(Base):
    __tablename__ = 'services'
    __table_args__ = {'extend_existing': True}
    sid = Column(String(30), primary_key=True)
    name = Column(String(30))
    local = Column(Boolean())

