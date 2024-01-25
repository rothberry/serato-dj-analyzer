import csv
from ipdb import set_trace
from pprint import pp


class CSVParser():

    def __init__(self, setlist=None, playlist_data=None, playlist_name=None) -> None:
        self.setlist = setlist # list of track dicts
        self.playlist_data = playlist_data # TODO change to meta_data
        self.playlist_name = playlist_name
        # ? Prob don't really need source 🤷‍♀️
        # self.source = ""

    def create_setlist(self, data_path):
        setlist = list()
        # self.source = data_path
        with open(data_path, newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for x, row in enumerate(csv_reader):
                row.pop("notes")
                row.pop("deck")
                setlist.append(row)
        self.playlist_data = setlist[0]
        self.setlist = setlist[1:]
        return setlist


class TxtParser():

    def __init__(self, setlist=None, playlist_name=None, playlist_data=[]):
        self.setlist = setlist
        self.playlist_data = playlist_data # TODO change to meta_data
        self.playlist_name = playlist_name
        # self.source = ""

    def create_setlist(self, data_path):
        setlist = list()
        # self.source = data_path
        with open(data_path) as txtfile:
            txt_reader = txtfile.read()
            txt_split = txt_reader.split("\n")
            # * From all of my sets, looks like serato .txt exports will always leave a 5 space gap between title/start_time
            # * may not be true for all tho
            self.set_playlist_data(txt_split[0],  txt_split[2])
            if not self.playlist_name:
                self.playlist_name = [
                    pd for pd in self.playlist_data if pd["name"] == "name"][0]["meta"]

            for i, row in enumerate(txt_split[:-1]):
                if i > 3:
                    row_dict = self.split_row_txt(row)
                    setlist.append(row_dict)
            self.setlist = setlist

    def set_playlist_data(self, column_row, data_row):
        column_list = [cl.strip()
                       for cl in self.remove_empties(column_row.split("     "))]
        column_list[0] = self.remove_ufeff(column_list[0])
        data_list = [dt.strip()
                     for dt in self.remove_empties(data_row.split("     "))]
        p_data = []
        for i, column_name in enumerate(column_list[:-1]):
            starting_idx = column_row.index(column_name) - 1
            try:
                meta_data = data_list[i]
            except IndexError:
                meta_data = ""
            # ? Could not append to self.p_d because then it makes it a class variable?
            p_data.append(
                {"name": column_name, "idx": starting_idx,  "meta": meta_data})
        self.playlist_data = p_data

    def split_row_txt(self, row_txt):
        row_dict = {}
        for i, col in enumerate(self.playlist_data):
            try:
                name, cur_idx, _ = col.values()
                next_idx = self.playlist_data[i + 1]["idx"]
            except IndexError:
                next_idx = None
            val = row_txt[cur_idx:next_idx].strip()
            row_dict[name] = val
        return row_dict

    def print_columns(self):
        col_names = [clm["name"] for clm in self.playlist_data]
        print(f"{col_names}")

    def print_setlist(self, tup):
        for tr in self.setlist:
            # print("")
            for x in tup:
                print(f"""{x}:\t{tr[x]}""")

    def get_indeces(self):
        return [clm["idx"] for clm in self.playlist_data]

    @staticmethod
    def remove_empties(lst):
        return list(filter(lambda x: len(x) > 0, lst))

    @staticmethod
    def remove_ufeff(clm):
        return clm.split("\ufeff")[1]

    @staticmethod
    def create_slug(clm):
        return "_".join(clm.strip().split(" "))