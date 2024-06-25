from flask_sqlalchemy import SQLAlchemy
from lib.helper import FlaskHelper
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


class Track(Base):
    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    bpm = db.Column(db.Float)
    key = db.Column(db.String)
    is_remix = db.Column(db.Boolean)
    # TODO How to differ between remixer and og artist?

    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=True)

    genre = db.relationship("Genre", backref="tracks")

    play_tracks = db.relationship("PlayTrack", backref="track")

    # ? Calculating instance methods?

    # @classmethod
    # def dynamic_create(cls, track_dict):
    #     # creates a track instance based off of args that align with the Track
    #     set_trace()
    #     return

    @staticmethod
    def fields():
        # returns all columns as tuple
        return ('id', 'title', 'bpm', 'key', 'is_remix')

    def times_played(self):
        return len(self.play_tracks)

    def average_length_played(self):
        pass

    def to_dict(self):
        dct = self.__dict__
        dct.pop("_sa_instance_state")
        return dct

    def __repr__(self):
        return f"Name: {self.title}"


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
        return f"Name: {self.name}"

    @classmethod
    def create_sets(cls, setlist):
        pl = Playlist(name=setlist.playlist_name)
        db.session.add(pl)
        db.session.commit()
        for meta_data in setlist.setlist:
            Track.create_track_data(meta_data, pl)
            # Track.create_track_data(db.session, meta_data, pl)


# TODO currently just for documenting, will need to find a way to normalize all artists given wildly different names
class Artist(db.Model):

    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    tracks = db.relationship(
        "Track", secondary=artist_track_association, backref="artists")

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self): return f'''id: {self.id} / name: {self.name}'''

# TODO also currently just for doc


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self): return f'''id: {self.id} / name: {self.name}'''
