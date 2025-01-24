from app import create_app
from lib.helper import FlaskHelper
from pprint import pp
from ipdb import set_trace
from lib.models import Playlist, Track, PlayTrack
from sys import argv
from py_term_helpers import center_string_stars, top_wrap


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        top_wrap("creating waves bro")

        pl = Playlist.query.all()[0]
        setlist = pl.show_setlist()

        
        set_trace()

        center_string_stars("DONE")
