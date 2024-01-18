from os import get_terminal_size, system


class TermHelper():
    term_size = get_terminal_size().columns

    @classmethod
    def top_wrap(cls, string, char="*"):
        system("clear")
        cls.term_wrap(string, char)

    @classmethod
    def term_wrap(cls, string, char="*"):
        cls.star_line(char)
        cls.center_string_stars(string, char)
        cls.star_line(char)

    @classmethod
    def star_line(cls, char="*"):
        print(char * cls.term_size)

    @classmethod
    def center_string_stars(cls, string, char="*"):
        half_size = (cls.term_size - len(string) - 2) / 2
        half_stars = char * int(half_size)
        print(f"{half_stars} {string} {half_stars}")


class FlaskHelper():

    @classmethod
    def find_or_create(cls, session, model, **kwargs):
        found_model = session.query(model).filter_by(**kwargs).one_or_none()
        if not found_model:
            return model(**kwargs)
        return found_model

    @classmethod
    def create_sets(cls, setlist):
        from models import db, Playlist, Track, Artist
        pl = Playlist(name=setlist.playlist_name)
        db.session.add(pl)
        db.session.commit()
        for track in setlist.setlist:
            Track.create_track_data(db.session, track, pl)

    @classmethod
    def create_track_data(cls, session, track, playlist):
        tr = FlaskHelper.find_or_create(session, cls, title=track["name"])
        session.add(tr)
        session.commit()
        pt = PlayTrack(track=tr, playlist=playlist,
                       start_time=track["start time"], end_time=track["end time"], playtime=track["playtime"])
        session.add(pt)
        session.commit()

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
