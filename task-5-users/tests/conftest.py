import pytest

from server import wsgi
from server.models import clear_clients, clients


@pytest.fixture
def app():
    return wsgi.app


@pytest.fixture(autouse=True)
def clean():
    clear_clients()
