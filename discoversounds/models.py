from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Boolean)

from discoversounds.database import Base
from discoversounds.helpers import shorten


class Artist(Base):
    __tablename__ = 'artists'
    __table_args__ = {'extend_existing': True, 'sqlite_autoincrement': True}
    artist_id = Column(Integer(), primary_key=True)
    artist_name = Column(String(255))

    def __init__(self, artist_name=None):
        self.artist_name = artist_name

    def __repr__(self):
        return 'Artist(artist_id=%r, artist_name=%r)' % (self.artist_id, self.artist_name)

    def __str__(self):
        return '<Artist %r>' % (self.artist_name)

    def __eq__(self, other):
        if not isinstance(other, Artist):
            return False
        else:
            return self.artist_name == other.artist_name and self.artist_id == other.artist_id

    def __hash__(self):
        return hash((self.artist_name, self.artist_id))


class ArtistRelation(Base):
    __tablename__ = 'artist_relations'
    __table_args__ = {'extend_existing': True}
    artist1 = Column(ForeignKey('artists.artist_id'), primary_key=True)
    artist2 = Column(ForeignKey('artists.artist_id'), primary_key=True)
    weight = Column(Integer())

    def __init__(self, artist1=None, artist2=None, weight=0):
        self.artist1 = artist1
        self.artist2 = artist2
        self.weight = weight

    def __repr__(self):
        return 'ArtistRelation(artist1=%r, artist2=%r, weight=%r)' % (self.artist1, self.artist2, self.weight)

    def __str__(self):
        return '<ArtistRelation %r, %r, (%r)>' % (self.artist1, self.artist2, self.weight)

    def __eq__(self, other):
        if not isinstance(other, ArtistRelation):
            return False
        else:
            return self.artist1 == other.artist1 and self.artist2 == other.artist2 and self.weight == other.weight

    def __hash__(self):
        return hash((self.artist1, self.artist2, self.weight))


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

    def __init__(self, vpid=None, epid=None, ipid=None, sid=None, title=None, synopsis=None, availability_from=None,
                 availability_to=None, has_songs=None):
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
            % (self.vpid, self.epid, self.ipid, self.sid, self.title, self.synopsis, self.availability_from,
               self.availability_to, self.has_songs)

    def __str__(self):
        return '<Show %r, %r, %r>' % (self.vpid, self.sid, shorten(self.title))

    def __eq__(self, other):
        if not isinstance(other, Show):
            return False
        else:
            return (
                self.vpid == other.vpid and
                self.epid == other.epid and
                self.ipid == other.ipid and
                self.sid == other.sid and
                self.title == other.title and
                self.synopsis == other.synopsis and
                self.availability_from == other.availability_from and
                self.availability_to == other.availability_to and
                self.has_songs == other.has_songs
            )

    def __hash__(self):
        return hash((
            self.vpid,
            self.epid,
            self.ipid,
            self.sid,
            self.title,
            self.synopsis,
            self.availability_from,
            self.availability_to,
            self.has_songs
        ))


class ShowToArtist(Base):
    __tablename__ = 'show_to_artist'
    __table_args__ = {'extend_existing': True}
    vpid = Column(String(40), primary_key=True)
    artist = Column(ForeignKey('artists.artist_id'), primary_key=True)
    expiry = Column(DateTime())

    def __init__(self, vpid=None, artist=None, expiry=None):
        self.vpid = vpid
        self.artist = artist
        self.expiry = expiry

    def __str__(self):
        return '<ShowToArtist %r, %r>' % (self.vpid, shorten(self.artist))

    def __repr__(self):
        return 'ShowToArtist(vpid=%r, artist=%r, expiry=%r)' % (self.vpid, self.artist, self.expiry)

    def __eq__(self, other):
        if not isinstance(other, ShowToArtist):
            return False
        else:
            return self.vpid == other.vpid and self.artist == other.artist and self.expiry == other.expiry

    def __hash__(self):
        return hash((self.vpid, self.artist, self.expiry))


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

    def __eq__(self, other):
        if not isinstance(other, Service):
            return False
        else:
            return self.sid == other.sid and self.name == other.name and self.local == other.local

    def __hash__(self):
        return hash((self.sid, self.name, self.local))
