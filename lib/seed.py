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
        FlaskHelper.commit_instances(test_genres)

        center_string_stars("SEEDING TEST FILES...")

        # parser creates a list of dicts for the set with title
        parser1 = CSVParser(playlist_name="parser1")
        parser1.create_setlist('sets/csv/1-20-2025.csv')

        # Will probably need another table(?) or something to keep track of all the current remix aliases that these dumb producers use.
        # maybe look for "re" prefix?
        remix_aliases = {"re", "remix", "edit", "flip", "redrum", "recrank"}

        FlaskHelper.dynamic_create(parser1)
        # Close the session
        db.session.close()
        center_string_stars("DON!")
