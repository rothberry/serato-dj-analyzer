from app import app
from models import db, Playlist, PlayTrack, Track, Artist, ArtistTrack, Genre
from py_term_helpers import TermHelper
from os import system

with app.app_context():
    TermHelper.top_wrap("UNSEEDING", "+")

    TermHelper.center_string_stars("Removing Temp Files..")
    system("rm -f ./temp/*")

    TermHelper.center_string_stars("Dropping..")
    # system("rm -f ./instance/*")
    # for mod in (PlayTrack, Playlist, Track, Artist, ArtistTrack, Genre):
    #     mod.query.delete()
    db.drop_all()

    TermHelper.center_string_stars("Creating Tables..")
    db.create_all()
    db.session.commit()

    db.session.close()
    TermHelper.center_string_stars("SHITSGONEYO!")
