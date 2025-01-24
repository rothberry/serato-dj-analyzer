from app import create_app
from lib.helper import FlaskHelper
from pprint import pp
from ipdb import set_trace
from lib.models import Playlist, Track, PlayTrack
from sys import argv
from py_term_helpers import center_string_stars, top_wrap
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        top_wrap("creating waves bro")

        pl = Playlist.query.all()[0]
        setlist = pl.show_setlist()

        bpms, keys, times = [], [], []
        # plt_vals = [{'bpm': tr["bpm"], "start": tr["start_time"], "end": tr["end_time"]} for tr in setlist[:3]]

        for tr in setlist:
            bpms.append(tr["bpm"])
            keys.append(int(tr["key"][:-1]))
            times.append(tr["start_time"])

        plt.plot(times, bpms, times, keys)
        
        plt.show()

        set_trace()

        center_string_stars("DONE")
