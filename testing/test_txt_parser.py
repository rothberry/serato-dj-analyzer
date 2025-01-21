import pytest
import os
from ipdb import set_trace
from lib.parser import TxtParser
from py_term_helpers import center_string_stars


""" 
TXT PARSER TESTS
- inits as a TXTParser
- has a setlist, playlist_name, playlist_data
    - setlist => list of track dicts
    - playlist_data => columns and divider locations
- can create the setlist as a list
  test data specs:
  - 74 tracks
  - cols:
    - ['name', 'start_time', 'end_time', 'playtime', 'deck']

 """

tp_test_data = TxtParser(playlist_name="test_data")
path_to_test = os.path.abspath(os.getcwd())

center_string_stars("txt parser")

def test_is_txt_parser():
    tp_empty = TxtParser()
    assert type(tp_empty) is TxtParser


def test_has_attr():
    assert tp_test_data.playlist_name is "test_data"
    assert tp_test_data.playlist_data == []
    assert tp_test_data.setlist is None


def test_create_setlist():
    tp_test_data.create_setlist(path_to_test + '/assets/test_data.txt')
    set_trace()
    assert all(x in ['name', 'start_time', 'end_time', 'playtime', 'deck']
               for x in tp_test_data.columns)
    assert type(tp_test_data.setlist)  is list
    assert type(tp_test_data.setlist[0])  is dict
