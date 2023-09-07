from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Playlist, PlayTrack, Track
from ipdb import set_trace
from parser import CSVParser, TxtParser
from helper import Helper

app = Flask(__name__)
# Replace with your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serato.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

# MAIN UPLOAD


@app.route("/upload", methods=["POST"])
def upload_setlist():
    # first detect if .txt or csv
    uploaded_file = request.files["file"]
    content_type = uploaded_file.content_type.split("/")[1]
    if content_type == "csv":
        Helper.center_string_stars("CSV UPLOADER", "+")
        set_trace()
    elif content_type == "plain":
        Helper.center_string_stars("TXT UPLOADER")
        set_trace()
    else:
        Helper.center_string_stars("BAD UPLOADER", "?")
        return make_response({"error": "Bad"}, 422)
    set_trace()
    return make_response({"message": "Succes"})

# TRACKS REST


@app.route("/tracks", methods=["GET", "POST"])
def index_create():
    if request.method == "GET":
        Helper.center_string_stars("INDEX")
        all_tracks = [track.to_dict() for track in Track.query.all()]
        return make_response(all_tracks)
    elif request.method == "POST":
        Helper.center_string_stars("CREATE")


@app.route("/tracks/<int:track_id>", methods=["GET"])
def show(track_id):
    track = Track.query.filter_by(id=track_id).first()
    if track:
        if request.method == "GET":
            Helper.center_string_stars("SHOW")
            return make_response(track.to_dict())
    else:
        return make_response({"error": f'Track of id: {track_id} not found'}, 404)


@app.route("/")
def base():
    return "Hi"


if __name__ == "__main__":
    port = 5555
    Helper.center_string_stars(f"Server Running on {port}")
    app.run(port=port, debug=True)
