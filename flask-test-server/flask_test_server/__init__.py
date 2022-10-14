from os.path import join, realpath, dirname
from flask import g, request
from flask import Flask

from datetime import timedelta

root_dir = realpath(join(dirname(__file__), ".."))

flask_templates_dir = realpath(join(dirname(__file__), "templates"))
flask_dataframes_dir = realpath(join(dirname(__file__), "dataframes"))

app = Flask(__name__, template_folder = flask_templates_dir)

app.config["TEMPLATES_DIR"] = flask_templates_dir
app.config["DATAFRAMES_DIR"] = flask_dataframes_dir
app.secret_key = "development key"

import flask_test_server.routes