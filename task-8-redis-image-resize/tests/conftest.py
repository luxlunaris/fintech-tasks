from api import wsgi
import pytest


@pytest.fixture
def app():
    return wsgi.app
