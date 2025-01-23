from flask_sqlalchemy import SQLAlchemy
from lib.helper import FlaskHelper, MiscHelper
from ipdb import set_trace

db = SQLAlchemy()
# Define a base class for declarative models
Base = db.Model

# TODO may add genre/artist/deck to either PlayTrack/Track or new models

artist_track_association = db.Table(
    'artist_track_association',
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id')),
    db.Column('track_id', db.Integer, db.ForeignKey('tracks.id'))
)


class PlayTrack(Base):
    __tablename__ = 'play_tracks'

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def playtime(self):
        # end - start time in secs (or millis)
        end_secs = MiscHelper.convert_ts_to_seconds(self.end_time)
        start_secs = MiscHelper.convert_ts_to_seconds(self.start_time)
        return end_secs - start_secs

    def to_dict(self):
        dct = self.__dict__
        dct.pop("_sa_instance_state")
        return dct

    def __repr__(self):
        return f"playid: {self.playlist_id} / trackid: {self.track_id}"


class Track(Base):
    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    bpm = db.Column(db.Float)
    key = db.Column(db.String)
    is_remix = db.Column(db.Boolean, default=False)
    # TODO How to differ between remixer and og artist?

    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=True)

    genre = db.relationship("Genre", backref="tracks")

    play_tracks = db.relationship("PlayTrack", backref="track")

    # ? Calculating instance methods?
    @staticmethod
    def fields():
        # returns all columns as tuple
        return ('id', 'title', 'bpm', 'key', 'is_remix')

    def times_played(self):
        return len(self.play_tracks)

    def average_length_played(self):
        pass

    def print_dict(self):
        dct = self.__dict__
        dct.pop("_sa_instance_state")
        return dct

    def __repr__(self):
        # return f'("id": {self.id},"title": {self.title},"key": {self.key},"genre_id": {self.genre_id},"bpm": {self.bpm},"is_remix": {self.is_remix})'
        # return f'({self.id},{self.title},{self.key},{self.genre_id},{self.bpm},{self.is_remix})'
        return f'({self.id}: {self.title})'


class Playlist(Base):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Define the relationship to the Track model
    tracks = db.relationship(
        "Track", secondary=PlayTrack.__table__, backref="playlists")
    play_tracks = db.relationship("PlayTrack", backref="playlist")

    # TODO Add all the total playlist metadata here?

    @property
    def get_tracks(self):
        return [(pt.track, pt) for pt in self.play_tracks]

    @property
    def track_count(self):
        return len(self.play_tracks)

    def show_setlist(self):
        tracklist = []
        for pt in self.play_tracks:
            tr = pt.track.__dict__
            tr["artists"] = [art.name for art in pt.track.artists]
            tr["genre"] = pt.track.genre.name
            if tr["_sa_instance_state"]:
                tr.pop("_sa_instance_state")
            tracklist.append(tr)
        return tracklist

    def to_dict(self, rel=False):
        tracks = [tr.to_dict() for tr in self.tracks]
        dct = self.__dict__
        dct.pop("_sa_instance_state")
        if rel:
            dct["tracks"] = tracks
        return dct

    def __repr__(self):
        return f"{self.id}: {self.name} #{self.track_count}"


# TODO currently just for documenting, will need to find a way to normalize all artists given wildly different names
class Artist(Base):

    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    tracks = db.relationship(
        "Track", secondary=artist_track_association, backref="artists")

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'({self.id}: {self.name})'

# TODO also currently just for doc


class Genre(Base):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'({self.id}: {self.name})'


class RemixAlias(Base):
    __tablename__ = "remix_alias"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'({self.id}: {self.name})'
