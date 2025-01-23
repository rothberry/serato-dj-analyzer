from app import create_app
from lib.helper import FlaskHelper
from pprint import pp
from ipdb import set_trace
from sys import argv
from py_term_helpers import center_string_stars, top_wrap


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        top_wrap("UPLOADING?")

        # TODO make gooder
        if len(argv) == 2:
            FlaskHelper.parse_to_create(
                filepath=argv[1])
        elif len(argv) == 3:
            FlaskHelper.parse_to_create(
                filepath=argv[1], playlist_name=argv[2])
        else:
            print("Need the 'filepath' and the optional playlist name as args")

        center_string_stars("DONE")
