# pylint: skip-file
from flask import Flask

app = Flask(__name__)

# register handlers
from .views import *  # noqa isort:skip
