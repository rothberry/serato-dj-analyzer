from app import app
from models import db, Base, Playlist, Track, PlayTrack
from pprint import pp
from ipdb import set_trace
from helper import TermHelper


with app.app_context():
    playlists = Playlist.query.all()
    tracks = Track.query.all()
    play_tracks = PlayTrack.query.all()
    # pt1, tr1, pl1 = [play_tracks[0], tracks[0], playlists[0]]
    TermHelper.top_wrap("DEBUG MODE")
    set_trace()

    TermHelper.center_string_stars("DONE")
