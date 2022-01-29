# pylint: skip-file
from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app)

# register handlers
from .views import *  # noqa isort:skip
