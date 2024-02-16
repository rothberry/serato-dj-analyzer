from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from lib.models import db, Playlist, PlayTrack, Track
from ipdb import set_trace
from lib.parser import CSVParser, TxtParser
from py_term_helpers import star_line, center_string_stars, top_wrap
import os
from pprint import pp
from time import strftime

# app = Flask(__name__)
# # Replace with your database URI
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sera2.db'
# basedir = os.path.abspath(os.path.dirname(__file__))
# # basedir = os.path.abspath(os.getcwd())
# path_to = os.path.join(basedir, 'instance', 'serato.db')
# star_line()
# print('sqlite:///' + path_to)
# star_line()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path_to

# MAIN UPLOAD
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config:
        app.config.from_mapping(test_config)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serato.db'
    app.config["TEMP_FOLDER"] = './temp'
    app.json.compact = False
    CORS(app)
    migrate = Migrate(app, db)
    db.init_app(app)

    from lib.routes import hello
    app.register_blueprint(hello)

    return app

if __name__ == "__main__":
    port = 5555
    top_wrap(f"Server Running on {port}")
    app = create_app()
    app.run(port=port, debug=True)
