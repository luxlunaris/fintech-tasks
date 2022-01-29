from http import HTTPStatus

import pytest
from flask import url_for

from server.models import add_client


def test_index_without_clients(client):
    response = client.get(url_for("index"))
    assert response.status_code == HTTPStatus.OK
    assert "<h1>Catalog of clients</h1>" in response.data.decode()


def test_index_with_clients(client):
    c = add_client("name", "num", "mail")
    response = client.get(url_for("index"))
    assert response.status_code == HTTPStatus.OK
    assert c.id[:5] in response.data.decode()
