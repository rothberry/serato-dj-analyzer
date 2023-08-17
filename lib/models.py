from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative models
Base = declarative_base()

class PlayTrack(Base):
    __tablename__ = 'play_tracks'

    id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlists.id'))
    track_id = Column(Integer, ForeignKey('tracks.id'))
    playtime = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"""playid: {self.playlist_id} / trackid: {self.track_id}"""


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define the relationship to the Track model
    tracks = relationship("Track", secondary=PlayTrack.__table__, back_populates="playlists")
    play_tracks = relationship("PlayTrack", backref=backref("playlist"))

    def __repr__(self):
        return f"Name: {self.name}"


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    title = Column(String)

    # Define the relationship to the Playlist model
    playlists = relationship("Playlist", secondary=PlayTrack.__table__, back_populates="tracks")
    play_tracks = relationship("PlayTrack", backref=backref("track"))

    def __repr__(self):
        return f"Name: {self.title}"
