# pylint: skip-file
from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

# register handlers
from .views import *  # noqa isort:skip
