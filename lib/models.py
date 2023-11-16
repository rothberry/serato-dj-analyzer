from flask_sqlalchemy import SQLAlchemy
from helper import FlaskHelper
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
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=True)

    # Define the relationship to the Playlist model
    playlists = db.relationship(
        "Playlist", secondary=PlayTrack.__table__, back_populates="tracks")
    # play_tracks = db.relationship("PlayTrack", backref=db.backref("track"))
    artists = db.relationship(
        "Artist", secondary=artist_track_association, backref=db.backref("tracks"))
    genre = db.relationship("Genre", backref=db.backref("tracks"))

    @classmethod
    def create_track_data(cls, meta_data, playlist):
        tr = FlaskHelper.find_or_create(db.session, cls, title=meta_data["name"])
        tr.bpm = meta_data["bpm"]
        tr.key = meta_data["key"]
        # TODO Will need to split artists (i.e. Wax Motif & BRKLYN) maybe already have artists in the db, and use this to check if they are there?
        artist = Artist(name=meta_data["artist"])
        artist.tracks.append(tr)
        db.session.add(tr)
        db.session.commit()
        pt = PlayTrack(track=tr, playlist=playlist, playtime=meta_data["playtime"])
        db.session.add(pt)
        db.session.commit()
        set_trace()

    # ? Calculating instance methods?
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
        "Track", secondary=PlayTrack.__table__, back_populates="playlists")
    play_tracks = db.relationship("PlayTrack", backref=db.backref("playlist"))

    # TODO Add all the total playlist metadata here?

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
