from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app import app
from models import db, Base, Playlist, Track, Artist, Genre
from helper import TermHelper
from parser import CSVParser, TxtParser
from pprint import pp
from ipdb import set_trace

with app.app_context():
    TermHelper.top_wrap("SEEDING", "+")

    TermHelper.center_string_stars("Dropping..")
    db.drop_all()

    TermHelper.center_string_stars("Creating Tables..")
    db.create_all()

    TermHelper.center_string_stars("Creating Test Playlist...")
    TermHelper.center_string_stars("Creating Test Genres...")
    TermHelper.center_string_stars("Creating Test ...")
    a1 = Artist(name="Phil")
    g1 = Genre(name="Trap")
    t1 = Track(title="Cool Song", bpm=125, key="Gm")
    db.session.add_all([a1, g1, t1])
    db.session.commit()

    a1.tracks.append(t1)
    db.session.add(a1)
    db.session.commit()

    t2 = Track(title="Gen Song", bpm=100, key="Am", genre_id=g1.id)
    db.session.add(t2)
    db.session.commit()

    set_trace()

    # Close the session
    db.session.close()
    TermHelper.center_string_stars("DON!")
