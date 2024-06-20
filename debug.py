from app import create_app
from lib.models import Playlist, Track, PlayTrack, Genre, Artist
from lib.parser import CSVParser, TxtParser
from lib.helper import FlaskHelper, MiscHelper
from pprint import pp
from ipdb import set_trace
from py_term_helpers import center_string_stars, top_wrap

app = create_app()
with app.app_context():
    playlists = Playlist.query.all()
    tracks = Track.query.all()
    play_tracks = PlayTrack.query.all()
    artists = Artist.query.all()
    genres = Genre.query.all()

    pt1, tr1, pl1 = [play_tracks[0], tracks[0], playlists[0]]
    set1 = pl1.show_setlist()
    top_wrap("DEBUG MODE")
    print([pl.track_count for pl in playlists])

    parser1 = TxtParser(playlist_name="parser1")
    parser1.create_setlist("sets/all_fields.txt")

    parser2 = CSVParser(playlist_name="parser2")
    parser2.create_setlist('sets/4-6-24.csv')

    p1_set = parser1.setlist
    p2_set = parser2.setlist

    set_trace()

    center_string_stars("DONE")
