import pytest
from app.models import Base
from db import engine
from app.wsgi import app


@pytest.fixture(autouse=True)
def init_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def app():
    return app
