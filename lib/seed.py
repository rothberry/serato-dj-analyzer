from ipdb import set_trace
from lib.models import Base, Playlist, Track, Artist, Genre
from py_term_helpers import star_line, center_string_stars, top_wrap
from pprint import pp
import sys
import os
from random import sample

# python -m lib.seed # to run seed for now

if __name__ == "__main__":
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    from app import create_app, db

    def create_instance(data):
        db.session.add_all(data)
        db.session.commit()

    app = create_app()
    with app.app_context():
        center_string_stars("SEEDING", "+")

        center_string_stars("Dropping..")
        db.drop_all()

        center_string_stars("Creating Tables..")
        db.create_all()

        genres = ['Trap', 'House', "Drum & Bass", "Techno"]

        center_string_stars("Creating Test Genres...")
        test_genres = []
        for g in genres:
            test_genres.append(Genre(name=g))
        create_instance(test_genres)

        center_string_stars("Creating Test Artists...")

        center_string_stars("Creating Test Tracks...")
        tracks = [
            {"title": "Test 1", "bpm": 140, "key": "Am",
                "is_remix": False, "genre_id": test_genres[0].id},
            {"title": "Test 2", "bpm": 70, "key": "Am",
                "is_remix": False, "genre_id": test_genres[0].id},
            {"title": "Test 3", "bpm": 150, "key": "Cm",
                "is_remix": True, "genre_id": test_genres[1].id},
            {"title": "Test 4", "bpm": 125, "key": "F",
                "is_remix": False, "genre_id": test_genres[2].id},
        ]
        test_tracks = []
        for t in tracks:
            test_track = Track(**t)
            test_tracks.append(test_track)

        create_instance(test_tracks)

        set_trace()

        center_string_stars("Creating Test Playlists...")
        # db.session.add_all([a1, g1, t1])
        # db.session.commit()

        # a1.tracks.append(t1)
        # db.session.add(a1)
        # db.session.commit()

        # t2 = Track(title="Gen Song", bpm=100, key="Am", genre_id=g1.id)
        # db.session.add(t2)
        # db.session.commit()

        set_trace()

        # Close the session
        db.session.close()
        center_string_stars("DON!")
