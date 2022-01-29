import pytest
import json

ns = "http://127.0.0.1:5000/movieratings/"


def test_users(client):
    assert "No user with such id" in client.get(ns + "users/1").get_data(as_text=True)

    assert b'{"users":[]}\n' == client.get(ns + "users").get_data()

    assert (
        "successfully"
        in client.post(
            ns + "users",
            data=json.dumps(dict(username="string", email="string")),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert '"email":"string"' in client.get(ns + "users").get_data(as_text=True)

    assert '"email":"string"' in client.get(ns + "users/1").get_data(as_text=True)

    assert (
        "successfully"
        in client.put(
            ns + "users/1",
            data=json.dumps(dict(username="string1", email="string1")),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert '"email":"string1"' in client.get(ns + "users/1").get_data(as_text=True)

    assert (
        "No user with such id"
        in client.put(
            ns + "users/21",
            data=json.dumps(dict(username="string1", email="string1")),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert "successfully" in client.delete(ns + "users/1").get_data(as_text=True)

    assert b'{"users":[]}\n' == client.get(ns + "users").get_data()


def test_movies(client):
    assert "No movie with such id" in client.get(ns + "movies/1").get_data(as_text=True)

    assert b'{"movies":[]}\n' == client.get(ns + "movies").get_data()

    assert (
        "successfully"
        in client.post(
            ns + "movies",
            data=json.dumps(dict(name="string", country="string", year=1000)),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert '"country":"string"' in client.get(ns + "movies").get_data(as_text=True)

    assert '"country":"string"' in client.get(ns + "movies/1").get_data(as_text=True)

    assert (
        "successfully"
        in client.put(
            ns + "movies/1",
            data=json.dumps(dict(name="string1", country="string1", year=1000)),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert '"name":"string1"' in client.get(ns + "movies/1").get_data(as_text=True)

    assert (
        "No movie with such id"
        in client.put(
            ns + "movies/21",
            data=json.dumps(dict(name="string1", country="string1", year=1000)),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert "successfully" in client.delete(ns + "movies/1").get_data(as_text=True)

    assert b'{"movies":[]}\n' == client.get(ns + "movies").get_data()


def test_ratings(client):
    assert "No rating with such ids" in client.get(ns + "ratings/1/1").get_data(
        as_text=True
    )

    assert "No such movie" in client.get(ns + "ratings/1").get_data(as_text=True)

    assert b'{"ratings":[]}\n' == client.get(ns + "ratings").get_data()

    assert (
        "successfully"
        in client.post(
            ns + "users",
            data=json.dumps(dict(username="string", email="string")),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert (
        "successfully"
        in client.post(
            ns + "movies",
            data=json.dumps(dict(name="string", country="string", year=1000)),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert b'{"ratings":[]}\n' in client.get(ns + "ratings/1").get_data()

    assert (
        "successfully"
        in client.post(
            ns + "ratings",
            data=json.dumps(dict(user_id=1, movie_id=1, value=10)),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert '"user_id":1' in client.get(ns + "ratings").get_data(as_text=True)

    assert (
        "successfully"
        in client.put(
            ns + "ratings/1/1",
            data=json.dumps(dict(user_id=1, movie_id=1, value=9)),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert '"value":9' in client.get(ns + "ratings/1/1").get_data(as_text=True)

    assert '"value":9' in client.get(ns + "ratings").get_data(as_text=True)

    assert (
        "No rating with such ids"
        in client.put(
            ns + "ratings/12/12",
            data=json.dumps(dict(user_id=1, movie_id=1, value=9)),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert (
        "Wrong rating"
        in client.post(
            ns + "ratings",
            data=json.dumps(dict(user_id=1, movie_id=1, value=12)),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert (
        "Wrong rating"
        in client.put(
            ns + "ratings/1/1",
            data=json.dumps(dict(user_id=1, movie_id=1, value=12)),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert "No rating with such ids" in client.get(ns + "ratings/10/10").get_data(
        as_text=True
    )

    assert "successfully" in client.delete(ns + "ratings/1/1").get_data(as_text=True)

    assert b'{"ratings":[]}\n' == client.get(ns + "ratings").get_data()
