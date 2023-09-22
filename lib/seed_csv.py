from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app import app
from models import db, Base, Playlist, Track
from helper import Helper
from parser import CSVParser, TxtParser
from pprint import pp
from ipdb import set_trace

with app.app_context():
    Helper.top_wrap("SEEDING", "+")
    csv_setlist = CSVParser(playlist_name="CSV Test")
    csv_setlist.create_setlist("./assets/test_data.csv")

    # txt_setlist = TxtParser(playlist_name="TXT Test")
    # txt_setlist.create_setlist("assets/test_data.txt")

    txt_setlist1 = TxtParser(playlist_name="TXT Test 5-21-2018-1")
    txt_setlist1.create_setlist("sets/5-21-2018 1.txt")

    txt_setlist2 = TxtParser()
    txt_setlist2.create_setlist("sets/12-29-2019.txt")

    Helper.center_string_stars("Dropping..")
    db.drop_all()

    Helper.center_string_stars("Creating Tables..")
    db.create_all()

    # def create_sets(setlist):
    #     pl = Playlist(name=setlist.playlist_name)
    #     db.session.add(pl)
    #     db.session.commit()
    #     for track in setlist.setlist:
    #         Track.create_track_data(db.session, track, pl)

    Helper.center_string_stars("Creating Tracks from csv...")
    Playlist.create_sets(csv_setlist)

    # Helper.center_string_stars("Creating Tracks from txt0...")
    # Playlist.create_sets(txt_setlist)

    Helper.center_string_stars("Creating Tracks from txt1...")
    Playlist.create_sets(txt_setlist1)
    Helper.center_string_stars("Creating Tracks from txt2...")
    Playlist.create_sets(txt_setlist2)

    # Close the session
    db.session.close()
    Helper.center_string_stars("DON!")
