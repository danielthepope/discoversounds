from sqlalchemy import (Column, DateTime, Integer, MetaData,
                        PrimaryKeyConstraint, String, Table, Boolean)

from discoversounds.database import Base
from discoversounds.helpers import shorten


class Show(Base):
    __tablename__ = 'shows'
    __table_args__ = {'extend_existing': True}
    vpid = Column(String(40), primary_key=True)
    epid = Column(String(40))
    ipid = Column(String(40))
    sid = Column(String(40), nullable=False)
    title = Column(String(255), nullable=False)
    synopsis = Column(String(1024))
    availability_from = Column(DateTime())
    availability_to = Column(DateTime())
    has_songs = Column(Boolean())

    def __init__(self, vpid=None, epid=None, ipid=None, sid=None, title=None, synopsis=None, availability_from=None, availability_to=None, has_songs=None):
        self.vpid = vpid
        self.epid = epid
        self.ipid = ipid
        self.sid = sid
        self.title = title
        self.synopsis = synopsis
        self.availability_from = availability_from
        self.availability_to = availability_to
        self.has_songs = has_songs

    def __repr__(self):
        return 'Show(vpid=%r, epid=%r, ipid=%r, sid=%r, title=%r, synopsis=%r, availability_from=%r, availability_to=%r, has_songs=%r)' \
            % (self.vpid, self.epid, self.ipid, self.sid, self.title, self.synopsis, self.availability_from, self.availability_to, self.has_songs)

    def __str__(self):
        return '<Show %r, %r, %r>' % (self.vpid, self.sid, shorten(self.title))


class ShowToArtist(Base):
    __tablename__ = 'show_to_artist'
    __table_args__ = {'extend_existing': True}
    vpid = Column(String(40), primary_key=True)
    artist = Column(String(255), primary_key=True)
    expiry = Column(DateTime())

    def __init__(self, vpid=None, artist=None, expiry=None):
        self.vpid = vpid
        self.artist = artist
        self.expiry = expiry

    def __str__(self):
        return '<ShowToArtist %r, %r>' % (self.vpid, shorten(self.artist))

    def __repr__(self):
        return 'ShowToArtist(vpid=%r, artist=%r, expiry=%r)' % (self.vpid, self.artist, self.expiry)

class Service(Base):
    __tablename__ = 'services'
    __table_args__ = {'extend_existing': True}
    sid = Column(String(40), primary_key=True)
    name = Column(String(40))
    local = Column(Boolean())

    def __init__(self, sid, name, local):
        self.sid = sid
        self.name = name
        self.local = local

    def __str__(self):
        return '<Service %r>' % (self.sid)

    def __repr__(self):
        return 'Service(sid=%r, name=%r, local=%r)' % (self.sid, self.name, self.local)
