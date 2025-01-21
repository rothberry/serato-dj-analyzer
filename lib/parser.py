import csv
from ipdb import set_trace
from pprint import pp
from py_term_helpers import top_wrap, center_string_stars as stars
from lib.helper import MiscHelper, FlaskHelper
from datetime import datetime, date, time, timezone


# TODO Things to add to the parser

class CSVParser():

    def __init__(self, playlist_name=None) -> None:
        self.setlist = []
        self.playlist_data = []
        self.playlist_name = playlist_name
        # ? Prob don't really need source 🤷‍♀️
        # self.source = ""

    def create_setlist(self, data_path):
        tz = datetime.now().astimezone().tzname()
        # self.source = data_path
        with open(data_path, newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)

            # * create playlist_data metadata
            data = next(csv_reader)
            # ! omit unneed fields
            for k in ("notes", 'deck'):
                data.pop(k, None)
            data["start_time"] = data.pop("start time")
            data["end_time"] = data.pop("end time")
            self.playlist_data = list(data.keys())

            # * create playlist_name if not
            self.playlist_name = self.playlist_name or data['name']

            start_date = data["start_time"].split(" ")[0]
            end_date = data["end_time"].split(" ")[0]
            strformat = '%m/%d/%Y %I:%M:%S %p %Z'
            utcformat = '%Y-%m-%d %H:%M:%S'
            for row in csv_reader:
                # normalize row before appending
                #   all lower
                #   correct types
                track_data = dict()
                for k in row:
                    v = row[k]
                    # print(row, k, v)
                    # ! Removed 'playtime' as column, will calc based off start/endtime
                    """ if k in ("playtime",) : row[k] = MiscHelper.convert_ts_to_seconds(row[k]) """
                    try:
                        if k in ("bpm", ):
                            v = float(v)
                        elif k in ("start time", "end time"):
                            # TODO have start and end time as UTC
                            # ? will assume start and end times are all on the same day
                            # if start_date == end_date:
                            k = k.replace(" ", "_")
                            v = datetime.strptime(
                                f'{start_date} {v} {tz}', strformat)
                            # else:
                            # ? will need to figure out if the playing past midnight
                        else:
                            v = v.lower()

                        # add new key value track data
                        # ! omit
                        if k not in ("notes", "deck"):
                            track_data[k] = v
                    except Exception as err:
                        stars((err, k, v))
                        set_trace()
                # set_trace()
                self.setlist.append(track_data)
        # set_trace()
        stars(
            f'setlist {self.playlist_name} created with {len(self.setlist)} tracks')
        return


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
                {"name": self.create_slug(column_name), "idx": starting_idx,  "meta": meta_data})
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

    @property
    def columns(self):
        col_names = [clm["name"] for clm in self.playlist_data]
        return col_names

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
