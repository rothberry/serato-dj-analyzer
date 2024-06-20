from ipdb import set_trace
from lib.models import Base, Playlist, Track, Artist, Genre, PlayTrack
from py_term_helpers import star_line, center_string_stars, top_wrap
from lib.helper import FlaskHelper
from lib.parser import TxtParser, CSVParser
from pprint import pp
import sys
import os
import re
from random import sample, shuffle, randint

# python -m lib.seed # to run seed for now

if __name__ == "__main__":
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    from app import create_app, db

    def commit_instances(data):
        if type(data) is list:
            db.session.add_all(data)
        else:
            db.session.add(data)
        db.session.commit()

    app = create_app()
    with app.app_context():
        top_wrap("SEEDING", "+")
        """

        center_string_stars("Dropping..")
        db.drop_all()

        center_string_stars("Creating Tables..")
        db.create_all()

        genres = ['Trap', 'House', "Drum & Bass", "Techno"]

        center_string_stars("Creating Test Genres...")
        test_genres = []
        for g in genres:
            test_genres.append(Genre(name=g))
        commit_instances(test_genres)

        center_string_stars("Creating Test Artists...")
        artists = ["Artist 1", "Artist 2", "Artist 3", "Artist 4"]
        test_artists = []
        for a in artists:
            test_artists.append(Artist(name=a))
        commit_instances(test_artists)

        center_string_stars("Creating Test Tracks...")
        tracks = [
            ({"title": "Test 1", "bpm": 140, "key": "Am",
             "is_remix": False, "genre_id": test_genres[0].id}, (1,)),
            ({"title": "Test 2", "bpm": 70, "key": "Am",
             "is_remix": False, "genre_id": test_genres[0].id}, (2,)),
            ({"title": "Test 3", "bpm": 150, "key": "Cm",
             "is_remix": True, "genre_id": test_genres[1].id}, (1, 2)),
            ({"title": "Test 4", "bpm": 125, "key": "F",
             "is_remix": False, "genre_id": test_genres[2].id}, (1, 3)),
        ]
        test_tracks = []
        for t in tracks:
            test_tracks.append(Track(**t[0]))

        commit_instances(test_tracks)

        # TODO mor effient seed logic
        for i, t in enumerate(tracks):
            artist_tracks = [test_artists[id] for id in t[1]]
            for at in artist_tracks:
                test_tracks[i].artists.append(at)

        commit_instances(test_tracks)

        center_string_stars("Creating Test Playlists...")
        playlists = ["Play1", "Play2", "Play3", "Play4", "Play5",]
        test_playlists = []
        for pl in playlists:
            t_playlist = Playlist(name=pl)
            commit_instances(t_playlist)
            p_tracks = sample(test_tracks, randint(1, len(test_tracks)))
            shuffle(p_tracks)
            play_time = "00:05:00"
            for pt in p_tracks:
                play_track = PlayTrack(
                    playlist_id=t_playlist.id,
                    track_id=pt.id,
                    playtime=play_time)
                commit_instances(play_track)

            test_playlists.append(t_playlist)

        commit_instances(test_playlists) """

        center_string_stars("SEEDING TEST FILES...")

        # seed the first file with all fields: artist/genre/etc
        # seed the second with missing fields and need to check if their is a similar entry in the track table

        parser1 = TxtParser(playlist_name="parser1")
        parser1.create_setlist("sets/all_fields.txt")

        parser2 = CSVParser(playlist_name="parser2")
        parser2.create_setlist('sets/4-6-24.csv')

        p1_set = parser1.setlist
        p2_set = parser2.setlist

        # parser_playlist_1 = Playlist(name="all_fields_txt")
        test_playlist = Playlist.query.first()

        # Will probably need another table(?) or something to keep track of all the current remix aliases that these dumb producers use.
        # maybe look for "re" prefix?
        remix_aliases = {"re", "remix", "edit", "flip", "redrum", "recrank"}

        for tr in p1_set:
            # track: title, bpm, key, is_remix
            #   title => has all lowercase, search in table
            #   remix => search title for remix keywords
            #   genre => as a finder func
            # artist(s): name
            #   separate individual artists

            # Look through track table for previous instance
            current_track = db.session.query(Track).filter_by(
                title=tr["name"].lower()).one_or_none()
            set_trace()
            if not current_track:

                current_track = Track(
                    title=tr["name"].lower(),

                )

        # Close the session
        db.session.close()
        center_string_stars("DON!")
