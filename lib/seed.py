from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Playlist, Track, PlayTrack
from helper import Helper
from parser import Parser
from pprint import pp
from ipdb import set_trace


if __name__ == "__main__":

    Helper.top_wrap("SEEDING")
    test_setlist = Parser()
    test_setlist.create_setlist("./assets/test_data.csv")

    # Create a SQLite in-memory database
    engine = create_engine('sqlite:///db/serato.db', echo=True)

    Base.metadata.drop_all(bind=engine)

    # Create the tables in the database
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    Helper.center_string_stars("Creating Test Playlist...")
    p1 = Playlist(name=test_setlist.playlist_data["name"])
    p2 = Playlist(name="Test Gym Playlist")
    session.add_all([p1, p2])
    session.commit()

    def create_track_data(setlist, playlist):
        for track in setlist:
            # tr = Track(title=track["name"])
            tr = Helper.find_or_create(session, Track, title=track["name"])
            session.add(tr)
            session.commit()
            pt = PlayTrack(track=tr, playlist=playlist,
                           start_time=track["start time"], end_time=track["end time"], playtime=track["playtime"])
            session.add(pt)
            session.commit()

    Helper.center_string_stars("Creating Tracks from csv...")
    create_track_data(test_setlist.setlist, p2)

    Helper.center_string_stars("Creating second playlist from csv...")
    create_track_data(test_setlist.setlist[:20], p1)

    # Close the session
    session.close()
    Helper.center_string_stars("DON!")
    # Helper.center_string_stars(f'Created {len(test_setlist.setlist)}')
    # Helper.center_string_stars(f'Created {len(session.query(Track).all())}')
