import csv
from pprint import pp
from ipdb import set_trace
from os import system
from helper import Helper


def create_setlist():
    set_list = list()
    with open("./assets/test_data.csv", newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for x, row in enumerate(csv_reader):
            # if x > 1:
                # set_trace()
                row.pop("notes")
                row.pop("deck")
                set_list.append(row)
    pp(set_list[:6])
    return set_list


Helper.top_wrap("Start")
create_setlist()
