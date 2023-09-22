from app import app
from models import db, Playlist, PlayTrack, Track, Artist, ArtistTrack, Genre
from helper import Helper
from os import system

with app.app_context():
    Helper.top_wrap("UNSEEDING", "+")

    Helper.center_string_stars("Removing Temp Files..")
    system("rm -f ./temp/*")

    Helper.center_string_stars("Dropping..")
    # system("rm -f ./instance/*")
    # for mod in (PlayTrack, Playlist, Track, Artist, ArtistTrack, Genre):
    #     mod.query.delete()
    db.drop_all()

    Helper.center_string_stars("Creating Tables..")
    db.create_all()
    db.session.commit()

    db.session.close()
    Helper.center_string_stars("SHITSGONEYO!")
