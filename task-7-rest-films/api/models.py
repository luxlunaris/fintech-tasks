from datetime import datetime

from flask import jsonify
from flask_restplus import fields

from db import Session, User, Movie, Rating
from .wsgi import api


USER = api.model(
    "User", {"username": fields.String, "email": fields.String}
)  # pragma: no cover


MOVIE = api.model(
    "Movie", {"name": fields.String, "country": fields.String, "year": fields.Integer}
)  # pragma: no cover


RATING = api.model(
    "Rating",
    {"user_id": fields.Integer, "movie_id": fields.Integer, "value": fields.Float},
)  # pragma: no cover


def users_list():
    s = Session()
    q = s.query(User).all()
    s.close()
    return jsonify(users=[user.toJSON() for user in q])


def movies_list():
    s = Session()
    q = s.query(Movie).all()
    s.close()
    return jsonify(movies=[movie.toJSON() for movie in q])


def ratings_list():
    s = Session()
    q = s.query(Rating).all()
    s.close()
    return jsonify(ratings=[rating.toJSON() for rating in q])


def movieratings_list(mid):
    s = Session()
    movie = s.query(Movie).filter_by(id=mid).first()
    q = s.query(Rating).filter_by(movie_id=mid)
    s.close()
    if not movie:
        return "No such movie", 400
    return jsonify(ratings=[rating.toJSON() for rating in q])


def create_user(data):
    s = Session()
    s.add(
        User(
            username=data["username"],
            email=data["email"],
            registration_date=datetime.now(),
        )
    )
    s.commit()
    s.close()
    return "User successfully created", 201


def create_movie(data):
    s = Session()
    s.add(Movie(name=data["name"], country=data["country"], year=data["year"]))
    s.commit()
    s.close()
    return "Movie successfully created", 201


def create_rating(data):
    s = Session()
    user, movie = (
        s.query(User).filter_by(id=data["user_id"]).first(),
        s.query(Movie).filter_by(id=data["movie_id"]).first(),
    )
    if not user:
        s.close()
        return "No such user", 400
    if not movie:
        s.close()
        return "No such movie", 400
    if data["value"] < 0 or data["value"] > 10:
        s.close()
        return "Wrong rating (must be in [0,10])", 400
    s.add(
        Rating(user_id=data["user_id"], movie_id=data["movie_id"], value=data["value"])
    )
    s.commit()
    s.close()
    return "Rating successfully created", 201


def get_user(uid):
    s = Session()
    user = s.query(User).filter_by(id=uid).first()
    s.close()
    if not user:
        return "No user with such id", 400
    return jsonify(user.toJSON())


def get_movie(mid):
    s = Session()
    movie = s.query(Movie).filter_by(id=mid).first()
    s.close()
    if not movie:
        return "No movie with such id", 400
    return jsonify(movie.toJSON())


def get_rating(mid, uid):
    s = Session()
    rating = s.query(Rating).filter_by(movie_id=mid, user_id=uid).first()
    s.close()
    if not rating:
        return "No rating with such ids", 400
    return jsonify(rating.toJSON())


def update_user(data, uid):
    s = Session()
    user = s.query(User).filter_by(id=uid).first()
    if not user:
        s.close()
        return "No user with such id", 400
    s.query(User).filter_by(id=uid).update(
        {"username": data["username"], "email": data["email"]}
    )
    s.commit()
    s.close()
    return "User successfully updated", 201


def update_movie(data, mid):
    s = Session()
    movie = s.query(Movie).filter_by(id=mid).first()
    if not movie:
        s.close()
        return "No movie with such id", 400
    s.query(Movie).filter_by(id=mid).update(
        {"name": data["name"], "country": data["country"], "year": data["year"]}
    )
    s.commit()
    s.close()
    return "Movie successfully updated", 201


def update_rating(mid, uid, data):
    s = Session()
    rating = s.query(Rating).filter_by(movie_id=mid, user_id=uid).first()
    if not rating:
        s.close()
        return "No rating with such ids", 400
    if data["value"] < 0 or data["value"] > 10:
        s.close()
        return "Wrong rating (must be in [0,10])", 400
    s.query(Rating).filter_by(movie_id=mid, user_id=uid).update(
        {"value": data["value"]}
    )
    s.commit()
    s.close()
    return "Rating successfully updated", 201


def delete_user(uid):
    s = Session()
    if not s.query(User).filter_by(id=uid):
        return "No user with such id", 400
    s.query(User).filter_by(id=uid).delete()
    s.query(Rating).filter_by(user_id=uid).delete()
    s.commit()
    s.close()
    return "User successfully deleted"


def delete_movie(mid):
    s = Session()
    if not s.query(Movie).filter_by(id=mid):
        return "No movie with such id", 400
    s.query(Movie).filter_by(id=mid).delete()
    s.query(Rating).filter_by(movie_id=mid).delete()
    s.commit()
    s.close()
    return "Movie successfully deleted"


def delete_rating(mid, uid):
    s = Session()
    if not s.query(Rating).filter_by(movie_id=mid, user_id=uid):
        return "No rating with such user and movie ids", 400
    s.query(Rating).filter_by(movie_id=mid, user_id=uid).delete()
    s.commit()
    s.close()
    return "Rating successfully deleted"
