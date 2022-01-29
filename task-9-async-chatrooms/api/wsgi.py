# pylint: skip-file
from aiohttp_swagger import *

from .app import create_app

app = create_app()
setup_swagger(app)
