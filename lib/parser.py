import csv
from ipdb import set_trace
from os import system
from helper import Helper


class Parser():

    def __init__(self, setlist=None, playlist_data=None) -> None:
        self.setlist = setlist
        self.playlist_data = playlist_data

    def create_setlist(self, data_path):
        setlist = list()
        with open(data_path, newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for x, row in enumerate(csv_reader):
                row.pop("notes")
                row.pop("deck")
                setlist.append(row)
        self.playlist_data = setlist[0]
        self.setlist = setlist[1:]
        return setlist
