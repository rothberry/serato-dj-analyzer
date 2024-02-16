import pytest
from ipdb import set_trace
from py_term_helpers import center_string_stars
from lib.models import *


class TestPlaylist():

  """ 
  - has a name & id
  - has many play_tracks
  - has tracks through play_tracks
  - given a parsed setlist (list of track dicts)
    - create a setlist 
      - aka PlayTracks(create) and Tracks(find or create)
  """
  p1 = Playlist()


  def test_playist_model(self):
    set_trace()

class TestTracks():
  """  """

  def test_track_data():
    pass