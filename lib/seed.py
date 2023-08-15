from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Playlist, Track, PlayTrack
from ipdb import set_trace

if __name__ == "__main__":

    # Create a SQLite in-memory database
    engine = create_engine('sqlite:///serato.db', echo=True)

    Base.metadata.drop_all(bind=engine)

    # Create the tables in the database
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    
    # Create playlists
    playlist1 = Playlist(name="My Favorites")
    playlist2 = Playlist(name="Party Mix")

    # Create tracks
    track1 = Track(title="Song 1")
    track2 = Track(title="Song 2")
    track3 = Track(title="Song 3")

    # Add playlists and tracks to the session
    session.add_all([playlist1, playlist2, track1, track2, track3])
    session.commit()

    # Create joins
    pt1 = PlayTrack(playlist_id=playlist1.id, track_id=track1.id,)
    pt2 = PlayTrack(playlist_id=playlist1.id, track_id=track2.id,)
    pt3 = PlayTrack(playlist_id=playlist1.id, track_id=track3.id,)
    pt4 = PlayTrack(playlist_id=playlist2.id, track_id=track3.id,)
    pt5 = PlayTrack(playlist_id=playlist1.id, track_id=track2.id,)
    session.add_all([pt1, pt2, pt3, pt4, pt5,])
    session.commit()

    # Close the session
    session.close()
    print("\nDON!\n")
