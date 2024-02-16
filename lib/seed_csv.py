from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app import app
from models import db, Base, Playlist, Track
from py_term_helpers import star_line, center_string_stars, top_wrap
from parser import CSVParser, TxtParser
from pprint import pp
from ipdb import set_trace

with app.app_context():
    top_wrap("SEEDING", "+")
    csv_setlist = CSVParser(playlist_name="CSV Test")
    csv_setlist.create_setlist("sets/10-7-23.csv")

    # txt_setlist = TxtParser(playlist_name="TXT Test")
    # txt_setlist.create_setlist("assets/test_data.txt")

    # txt_setlist1 = TxtParser(playlist_name="TXT Test 5-21-2018-1")
    # txt_setlist1.create_setlist("sets/5-21-2018 1.txt")

    # txt_setlist2 = TxtParser()
    # txt_setlist2.create_setlist("sets/12-29-2019.txt")

    center_string_stars("Dropping..")
    db.drop_all()

    center_string_stars("Creating Tables..")
    db.create_all()

    center_string_stars("Creating Tracks from csv...")
    Playlist.create_sets(csv_setlist)

    # center_string_stars("Creating Tracks from txt0...")
    # Playlist.create_sets(txt_setlist)

    center_string_stars("Creating Tracks from txt1...")
    Playlist.create_sets(txt_setlist1)
    center_string_stars("Creating Tracks from txt2...")
    Playlist.create_sets(txt_setlist2)

    # Close the session
    db.session.close()
    center_string_stars("DON!")
