from flask_sqlalchemy import SQLAlchemy
from helper import Helper

db = SQLAlchemy()
# Define a base class for declarative models
Base = db.Model

# TODO may add genre/artist/deck to either PlayTrack/Track or new models


class PlayTrack(Base):
    __tablename__ = 'play_tracks'

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'))
    playtime = db.Column(db.String)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        dct = self.__dict__
        dct.pop("_sa_instance_state")
        return dct

    def __repr__(self):
        return f"playid: {self.playlist_id} / trackid: {self.track_id}"


class Playlist(Base):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Define the relationship to the Track model
    tracks = db.relationship(
        "Track", secondary=PlayTrack.__table__, back_populates="playlists")
    play_tracks = db.relationship("PlayTrack", backref=db.backref("playlist"))

    # TODO Add all the total playlist metadata here?

    def to_dict(self):
        dct = self.__dict__
        dct.pop("_sa_instance_state")
        return dct

    def __repr__(self):
        return f"Name: {self.name}"


class Track(Base):
    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    # Define the relationship to the Playlist model
    playlists = db.relationship(
        "Playlist", secondary=PlayTrack.__table__, back_populates="tracks")
    play_tracks = db.relationship("PlayTrack", backref=db.backref("track"))

    @classmethod
    def create_track_data(cls, session, track, playlist):
        tr = Helper.find_or_create(session, cls, title=track["name"])
        session.add(tr)
        session.commit()
        pt = PlayTrack(track=tr, playlist=playlist,
                       start_time=track["start time"], end_time=track["end time"], playtime=track["playtime"])
        session.add(pt)
        session.commit()

    def to_dict(self):
        dct = self.__dict__
        dct.pop("_sa_instance_state")
        return dct

    def __repr__(self):
        return f"Name: {self.title}"
