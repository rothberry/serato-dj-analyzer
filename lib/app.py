from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Playlist, PlayTrack, Track
from ipdb import set_trace
from helper import Helper

app = Flask(__name__)
# Replace with your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serato.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)
db.init_app(app)


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
    app.run(port=5555, debug=True)
