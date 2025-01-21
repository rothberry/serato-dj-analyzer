from app import app
from models import db, Playlist, PlayTrack, Track, Artist, ArtistTrack, Genre
from py_term_helpers import center_string_stars, top_wrap
from os import system

with app.app_context():
    top_wrap("UNSEEDING", "+")

    center_string_stars("Removing Temp Files..")
    system("rm -f ./temp/*")

    center_string_stars("Dropping..")
    # system("rm -f ./instance/*")
    # for mod in (PlayTrack, Playlist, Track, Artist, ArtistTrack, Genre):
    #     mod.query.delete()
    db.drop_all()

    center_string_stars("Creating Tables..")
    db.create_all()
    db.session.commit()

    db.session.close()
    center_string_stars("SHITSGONEYO!")
