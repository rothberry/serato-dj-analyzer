import pytest
from ipdb import set_trace
from py_term_helpers import center_string_stars
from lib.models import *



""" 
- has a name & id
- has many play_tracks
- has tracks through play_tracks
- given a parsed setlist (list of track dicts)
    - create a setlist 
    - aka PlayTracks(create) and Tracks(find or create)
"""

def test_models_all(app):
    set_trace()


# def test_playist_model(app):
#     set_trace()
