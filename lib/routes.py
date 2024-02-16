from flask import current_app, Blueprint, render_template, make_response, request
from lib.models import db, Playlist, PlayTrack, Track
from ipdb import set_trace
from lib.parser import CSVParser, TxtParser
from py_term_helpers import star_line, center_string_stars, top_wrap
import os
from pprint import pp
from time import strftime


flask_app = Blueprint('flask_app', __name__)


@flask_app.route('/')
def index():
    return "HELLLLLLLO WORLD"


@flask_app.route("/upload", methods=["POST"])
def upload_setlist():
    # save file to temp (with timestamp)
    # detect if .txt or csv
    # create correct parser
    # create_setlist
    # delete temp file? Or chron job to delete?
    uploaded_file = request.files["file"]
    playlist_name = request.form["playlist_name"]
    content_type = uploaded_file.content_type.split("/")[1]
    timestr = strftime("%Y%m%d-%H%M%S")
    temp_path = os.path.join(
        app.config["TEMP_FOLDER"], f"{timestr}-{uploaded_file.filename}")
    uploaded_file.save(temp_path)

    if content_type in ["csv", "plain"]:
        center_string_stars(
            "CSV" if content_type == "csv" else "TXT", "+" if content_type == "csv" else "-")
        newParser = CSVParser(playlist_name=playlist_name) if content_type == "csv" else TxtParser(
            playlist_name=playlist_name)
        newParser.create_setlist(temp_path)
        Playlist.create_sets(newParser)
    else:
        center_string_stars("BAD UPLOADER", "?")
        return make_response({"error": "Bad"}, 422)
    return make_response({"message": "Succes"})

# PLAYLIST REST


@flask_app.route("/playlists", methods=["GET"])
def index_playlist():
    center_string_stars("PLAYLIST INDEX")
    all_pl = [playlist.to_dict(True) for playlist in Playlist.query.all()]
    return make_response(all_pl)


# TRACKS REST

@flask_app.route("/tracks", methods=["GET", "POST"])
def index_create():
    if request.method == "GET":
        center_string_stars("TRACKS INDEX")
        all_tracks = [track.to_dict() for track in Track.query.all()]
        return make_response(all_tracks)
    elif request.method == "POST":
        center_string_stars("CREATE")


@flask_app.route("/tracks/<int:track_id>", methods=["GET"])
def show(track_id):
    track = Track.query.filter_by(id=track_id).first()
    if track:
        if request.method == "GET":
            center_string_stars("SHOW")
            return make_response(track.to_dict())
    else:
        return make_response({"error": f'Track of id: {track_id} not found'}, 404)
