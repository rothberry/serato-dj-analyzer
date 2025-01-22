from ipdb import set_trace
from py_term_helpers import center_string_stars as stars


class FlaskHelper():

    @classmethod
    def find_or_create(cls, session, model, **kwargs):
        found_model = session.query(model).filter_by(**kwargs).one_or_none()
        if not found_model:
            return model(**kwargs)
        return found_model

    @classmethod
    def commit_instances(cls, data):
        from app import db
        if type(data) is list:
            db.session.add_all(data)
        else:
            db.session.add(data)
        db.session.commit()

    # TODO move this into the Playlist Model?

    @classmethod
    def dynamic_create(cls, parser_dict):
        # creates a track instance based off of args that align with the Track
        from lib.models import Playlist, Track, Artist, Genre, PlayTrack
        from app import db

        try:

            pl = Playlist(name=parser_dict.playlist_name)
            cls.commit_instances(pl)

            for tr in parser_dict.setlist:
                # track: title, bpm, key, is_remix
                #   title => has all lowercase, search in table
                #   remix => search title for remix keywords
                #   genre => as a finder func
                # artist(s): name
                #   separate individual artists

                # Look through track table for previous instance
                current_track = db.session.query(Track).filter_by(
                    title=tr["name"].lower()).one_or_none()
                if current_track:
                    print("FOUND TRACK IN DATABASE")
                else:
                    print("CREATING NEW TRACK")
                    tr_genre, tr_artist = None, None
                    # TODO refactor into more dynamic setters
                    if tr.get("genre"):
                        tr_genre = Genre.query.filter_by(
                            name=tr["genre"]).one_or_none()
                        if not tr_genre:
                            tr_genre = Genre(name=tr["genre"])
                            cls.commit_instances(tr_genre)
                            tr.pop("genre")

                    # TODO currently will not separate artists in collabs/remixees
                    if tr.get("artist"):
                        tr_artist = Artist.query.filter_by(
                            name=tr["artist"]).one_or_none()
                        if not tr_artist:
                            tr_artist = Artist(name=tr["artist"])
                            cls.commit_instances(tr_artist)
                            tr.pop("artist")
                    new_track = Track(
                        title=tr["name"], bpm=tr["bpm"], key=MiscHelper.camelot_converter(tr["key"]))
            set_trace()
        except Exception as err:
            set_trace()

            # Needs to create/find play_track

        return

    @classmethod
    def separate_artists(cls, artists):
        # effienctly separate artists in string
        pass
    # Moved to Playlist Model

    @classmethod
    def create_sets(cls, setlist):
        from models import db, Playlist
        pl = Playlist(name=setlist.playlist_name)
        db.session.add(pl)
        db.session.commit()
        for track in setlist.setlist:
            cls.create_track_data(track, pl)

    # Moved to Track Model
    @classmethod
    def create_track_data(cls, track, playlist):
        from models import db, PlayTrack
        tr = FlaskHelper.find_or_create(db.session, cls, title=track["name"])
        db.session.add(tr)
        db.session.commit()
        pt = PlayTrack(track=tr, playlist=playlist,
                       start_time=track["start time"], end_time=track["end time"], playtime=track["playtime"])
        db.session.add(pt)
        db.session.commit()

    @classmethod
    def test_kwargs(cls, first, **kwargs):
        return kwargs


class MiscHelper():

    @classmethod
    def convert_ts_to_seconds(cls, time_str):
        hours, minutes, seconds = time_str.split(":")
        total = int(seconds) + int(minutes) * 60 + int(hours) * 3600
        return total

    @classmethod
    def convert_seconds_to_ts(cls, seconds):
        from datetime import timedelta
        return str(timedelta(seconds=seconds))

    @staticmethod
    def camelot_dict():
        camelot = {
            # minor
            "1a": ("abm", "g#m"),
            "2a": ("ebm", "d#m"),
            "3a": ("bbm", "a#m"),
            "4a": ("fm",),
            "5a": ("cm",),
            "6a": ("gm",),
            "7a": ("dm",),
            "8a": ("am",),
            "9a": ("em",),
            "10a": ("bm",),
            "11a": ("gbm", "f#m"),
            "12a": ("dbm", "c#m"),
            # major
            "1b": ("b",),
            "2b": ("gb", "f#"),
            "3b": ("db", "c#"),
            "4b": ("ab", "g#"),
            "5b": ("eb", "d#"),
            "6b": ("bb", "a#"),
            "7b": ("f", ),
            "8b": ("c", ),
            "9b": ("g", ),
            "10b": ("d", ),
            "11b": ("a", ),
            "12b": ("e", ),
        }
        return camelot

    @classmethod
    def camelot_converter(cls, key):
        try:
            if cls.camelot.get(key):
                return key
            else:
                found_key = [(cam, keys)
                             for cam, keys in cls.camelot.items() if key in keys][0]
                return found_key[0]
        except KeyError:
            return None
