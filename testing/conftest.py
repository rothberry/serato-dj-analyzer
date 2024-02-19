import pytest
from app import create_app
from ipdb import set_trace
from lib.models import *
from py_term_helpers import center_string_stars
import os


@pytest.fixture
def app():
    center_string_stars("created app", "+")
    app = create_app({
        'TESTING': True,
        "DEBUG": True
    })
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI=os.path.join(app.instance_path, 'test_serato.db')) 
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def create_seed_data(app):
    with app.app_context():
        p1 = Playlist(name="play1")
        test_tracks = []
