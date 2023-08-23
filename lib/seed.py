from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Playlist, Track
from helper import Helper
from parser import CSVParser, TxtParser
from pprint import pp
from ipdb import set_trace


if __name__ == "__main__":

    Helper.top_wrap("SEEDING", "+")
    csv_setlist = CSVParser(playlist_name="CSV Test")
    csv_setlist.create_setlist("./assets/test_data.csv")

    txt_setlist = TxtParser(playlist_name="TXT Test")
    txt_setlist.create_setlist("assets/test_data.txt")

    txt_setlist1 = TxtParser(playlist_name="TXT Test 5-21-2018-1")
    txt_setlist1.create_setlist("sets/5-21-2018 1.txt")

    txt_setlist2 = TxtParser()
    txt_setlist2.create_setlist("sets/12-29-2019.txt")

    # Create a SQLite in-memory database
    engine = create_engine('sqlite:///db/serato.db', echo=True)

    Helper.center_string_stars("Dropping..")
    Base.metadata.drop_all(bind=engine)

    Helper.center_string_stars("Creating Tables..")
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    def create_sets(setlist):
        pl = Playlist(name=setlist.playlist_name)
        session.add(pl)
        session.commit()
        for track in setlist.setlist:
            Track.create_track_data(session, track, pl)

    Helper.center_string_stars("Creating Tracks from csv...")
    create_sets(csv_setlist)

    Helper.center_string_stars("Creating Tracks from txt0...")
    create_sets(txt_setlist)

    Helper.center_string_stars("Creating Tracks from txt1...")
    create_sets(txt_setlist1)
    Helper.center_string_stars("Creating Tracks from txt2...")
    create_sets(txt_setlist2)

    # Close the session
    session.close()
    Helper.center_string_stars("DON!")
