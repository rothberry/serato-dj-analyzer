from app import create_app
from lib.models import db, Genre, RemixAlias
from py_term_helpers import center_string_stars
from lib.helper import FlaskHelper
from pprint import pp
import os
import sys
from ipdb import set_trace


if __name__ == "__main__":
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)

    app = create_app()
    with app.app_context():
        center_string_stars("Dropping Constant(ish) tables..")
        Genre.__table__.drop(db.engine, checkfirst=True)
        RemixAlias.__table__.drop(db.engine, checkfirst=True)

        center_string_stars("Creating Constant(ish) tables..")
        Genre.__table__.create(db.engine)
        RemixAlias.__table__.create(db.engine)

        genres = ['trap', 'house', "drum and bass", "techno"]

        center_string_stars("Creating Test Genres...")
        test_genres = []
        for g in genres:
            test_genres.append(Genre(name=g))
        FlaskHelper.commit_instances(test_genres)

        remix_alias = {"re", "remix", "edit", "flip", "redrum", "recrank"}

        center_string_stars("Creating Test Remixes...")
        remixes = []
        for remix in remix_alias:
            remixes.append(RemixAlias(name=remix))
        FlaskHelper.commit_instances(remixes)

        db.session.close()
        center_string_stars("DON!")
