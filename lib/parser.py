import csv
from ipdb import set_trace
from pprint import pp
from helper import Helper


class CSVParser():

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


class TxtParser():
    # TODO needs to be modular for additional columns
    # TODO can abstract the columns of the export from the top of txt
    # TODO make find index of starting character on columns to get the starting index for each row, this may account for blank spaces that get removed

    def __init__(self, setlist=None, playlist_data=None, columns=[]) -> None:
        self.setlist = setlist
        self.playlist_data = playlist_data
        self.columns = columns

    def create_setlist(self, data_path):
        setlist = list()
        with open(data_path) as txtfile:
            txt_reader = txtfile.read()
            txt_split = txt_reader.split("\n")
            # * From all of my sets, looks like serato .txt exports will always leave a 5 space gap between title/start_time
            # * may not be true for all tho
            txt_test = self.remove_empties(txt_split[4].split("     "))
            txt_test = [clm.strip() for clm in txt_test]

            self.set_columns(txt_split[0])
            for i, row in enumerate(txt_split[:-1]):
                if i > 3:
                    row_dict = self.split_row_txt(row)
                    setlist.append(row_dict)
            self.setlist = setlist

    def set_columns(self, column_row):
        column_list = [cl.strip()
                       for cl in self.remove_empties(column_row.split("     "))]
        column_list[0] = self.remove_ufeff(column_list[0])
        for column_name in column_list[:-1]:
            starting_idx = column_row.index(column_name) - 1
            self.columns.append({"name": column_name, "idx": starting_idx})

    def split_row_txt(self, row_txt):
        row_dict = {}
        for i, col in enumerate(self.columns):
            try:
                name, cur_idx = col.values()
                next_idx = self.columns[i + 1]["idx"]
            except IndexError:
                next_idx = None
            val = row_txt[cur_idx:next_idx].strip()
            row_dict[name] = val
        return row_dict

    def print_columns(self):
        col_names = [clm["name"] for clm in self.columns]
        print(f"{col_names}")

    def print_setlist(self, tup):
        for tr in self.setlist:
            # print("")
            for x in tup:
                print(f"""{x}:\t{tr[x]}""")
                

    def get_indeces(self):
        return [clm["idx"] for clm in self.columns]

    @staticmethod
    def remove_empties(lst):
        return list(filter(lambda x: len(x) > 0, lst))

    @staticmethod
    def remove_ufeff(clm):
        return clm.split("\ufeff")[1]

    @staticmethod
    def create_slug(clm):
        return "_".join(clm.strip().split(" "))


Helper.top_wrap("Parser?")

Helper.star_line("+")
txt1 = TxtParser(playlist_data="TextTest1")
txt1.create_setlist("assets/test_data.txt")
txt1.print_columns()
txt1.print_setlist(("name",))

Helper.star_line("-")
txt2 = TxtParser(playlist_data="TextTest2")
txt2.create_setlist("sets/5-21-2018 1.txt")
txt2.print_columns()
txt2.print_setlist(("name", "artist"))

set_trace()
