from ipdb import set_trace
from lib.models import Base, Playlist, Track, Artist, Genre, PlayTrack
from py_term_helpers import star_line, center_string_stars, top_wrap
from lib.helper import FlaskHelper, MiscHelper
from lib.parser import TxtParser, CSVParser
from pprint import pp
import sys
import os
import re
from random import sample, shuffle, randint

# python -m lib.seed # to run seed for now

if __name__ == "__main__":
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    from app import create_app, db

    def commit_instances(data):
        if type(data) is list:
            db.session.add_all(data)
        else:
            db.session.add(data)
        db.session.commit()

    app = create_app()
    with app.app_context():
        top_wrap("SEEDING", "+")
        center_string_stars("Dropping..")
        db.drop_all()

        center_string_stars("Creating Tables..")
        db.create_all()

        genres = ['trap', 'house', "drum & bass", "techno"]

        center_string_stars("Creating Test Genres...")
        test_genres = []
        for g in genres:
            test_genres.append(Genre(name=g))
        commit_instances(test_genres)

        center_string_stars("SEEDING TEST FILES...")

        parser1 = CSVParser(playlist_name="parser1")
        parser1.create_setlist('sets/csv/4-5-24.csv')

        parser2 = CSVParser(playlist_name="parser2")
        parser2.create_setlist('sets/csv/4-6-24.csv')

        p1_set = parser1.setlist
        p2_set = parser2.setlist

        test_playlist_1 = Playlist(name="p1")
        test_playlist_2 = Playlist(name="p2")

        # Will probably need another table(?) or something to keep track of all the current remix aliases that these dumb producers use.
        # maybe look for "re" prefix?
        remix_aliases = {"re", "remix", "edit", "flip", "redrum", "recrank"}

        for tr in p2_set:
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
                if tr.get("genre"):
                    tr_genre = Genre.query.filter_by(
                        name=tr["genre"]).one_or_none()
                    if not tr_genre:
                        tr_genre = Genre(name=tr["genre"])
                        commit_instances(tr_genre)
                        tr.pop("genre")

                if tr.get("artist"):
                    tr_artist = Artist.query.filter_by(
                        name=tr["artist"]).one_or_none()
                    if not tr_artist:
                        tr_artist = Artist(name=tr["artist"])
                        commit_instances(tr_artist)
                        tr.pop("artist")
                set_trace()
                current_track = Track(
                    title=tr["name"], bpm=tr["bpm"], key=MiscHelper.camelot_converter(tr["key"]),)

            # Needs to create/find play_track
            set_trace()

        # Close the session
        db.session.close()
        center_string_stars("DON!")
