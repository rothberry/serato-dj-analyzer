class FlaskHelper():

    @classmethod
    def find_or_create(cls, session, model, **kwargs):
        found_model = session.query(model).filter_by(**kwargs).one_or_none()
        if not found_model:
            return model(**kwargs)
        return found_model

    # TODO move this into the Playlist Model?
    @classmethod
    def dynamic_create(cls, track_dict):
        from ipdb import set_trace
        # creates a track instance based off of args that align with the Track
        set_trace()
        return

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

    @classmethod
    def camelot_converter(cls, key):
        camelot = {
            # minor
            "abm": "1A", "g#m": "1A",
            "ebm": "2A", "d#m": "2A",
            "bbm": "3A", "a#m": "3A",
            "fm": "4A",
            "cm": "5A",
            "gm": "6A",
            "dm": "7A",
            "am": "8A",
            "em": "9A",
            "bm": "10A",
            "f#m": "11A", "gbm": "11A",
            "dbm": "12A", "c#m": "12A",
            # major
            "b": "1B",
            "f#": "2B", "gb": "2B",
            "db": "3B", "c#": "3B",
            "ab": "4B", "g#": "4B",
            "eb": "5B", "d#": "5B",
            "bb": "6B", "a#": "6B",
            "f": "7B",
            "c": "8B",
            "g": "9B",
            "d": "10B",
            "a": "11B",
            "e": "12B",
        }
        return camelot[key.lower()]
    
