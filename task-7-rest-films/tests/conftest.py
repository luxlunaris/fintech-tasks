from api import wsgi
from db import Base, engine
import pytest


@pytest.fixture
def app():
    return wsgi.app


@pytest.fixture(autouse=True)
def wipe_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
