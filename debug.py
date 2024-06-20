from app import create_app
from lib.models import Playlist, Track, PlayTrack, Genre, Artist
from lib.parser import CSVParser, TxtParser
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

    all_fields = TxtParser(playlist_name="all_fields")
    all_fields.create_setlist("sets/all_fields.txt")

    set_trace()

    center_string_stars("DONE")
