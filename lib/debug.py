from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Playlist, Track, PlayTrack
from pprint import pp
from ipdb import set_trace
from helper import Helper


if __name__ == "__main__":
    engine = create_engine('sqlite:///db/serato.db', echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    playlists = session.query(Playlist).all()
    tracks = session.query(Track).all()
    play_tracks = session.query(PlayTrack).all()
    Helper.top_wrap("DEBUG MODE")
    set_trace()

    Helper.center_string_stars("DONE")
