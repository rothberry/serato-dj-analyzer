from app import app
from models import db, Base, Playlist, Track, Genre, Remix
from py_term_helpers import center_string_stars
from parser import CSVParser, TxtParser
from lib.helper import FlaskHelper
from pprint import pp
from ipdb import set_trace

with app.app_context():
    # center_string_stars("Dropping..")
    # db.drop_all()

    # center_string_stars("Creating Tables..")
    # db.create_all()

    genres = ['trap', 'house', "drum & bass", "techno"]

    center_string_stars("Creating Test Genres...")
    test_genres = []
    for g in genres:
        test_genres.append(Genre(name=g))
    FlaskHelper.commit_instances(test_genres)

    # Close the session
    db.session.close()
    center_string_stars("DON!")
