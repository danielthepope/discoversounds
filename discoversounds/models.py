from sqlalchemy import (Column, DateTime, Integer, MetaData,
                        PrimaryKeyConstraint, String, Table)

from discoversounds.database import Base


class Show(Base):
    __tablename__ = 'shows'
    vpid = Column(String(30), primary_key=True)
    epid = Column(String(30))
    sid = Column(String(30), nullable=False)
    title = Column(String(255), nullable=False)
    synopsis = Column(String(1024))
    availability_from = Column(DateTime())
    availability_to = Column(DateTime())


class ShowToArtist(Base):
    __tablename__ = 'show_to_artist'
    vpid = Column(String(30), primary_key=True)
    artist = Column(String(255), primary_key=True)
    count = Column(Integer())
    expiry = Column(DateTime())

    def __init__(self, vpid, artist, count=1, expiry=None):
        self.vpid = vpid
        self.artist = artist
        self.count = count
        self.expiry = expiry
