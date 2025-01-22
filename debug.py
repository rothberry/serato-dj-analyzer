from app import create_app
from lib.models import Playlist, Track, PlayTrack, Genre, Artist, RemixAlias
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
    remix_alias = RemixAlias.query.all()
    top_wrap("DEBUG MODE")

    set_trace()
    

    center_string_stars("DONE")
