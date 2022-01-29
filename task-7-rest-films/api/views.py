from flask import request
from flask_restplus import Resource

import api.models as m

from .wsgi import api

ns = api.namespace(
    "movieratings", description="Operations with users, movies and ratings"
)


@ns.route("/users")
class Users(Resource):
    def get(self):
        """Returns list of all users existing in database"""
        return m.users_list()

    @api.expect(m.USER, validate=True)
    def post(self):
        """Creates user with passed json data"""
        return m.create_user(request.get_json())


@ns.route("/users/<int:user_id>")
class UsersOperations(Resource):
    def get(self, user_id):
        """Returns user found by passed user id"""
        return m.get_user(user_id)

    @api.expect(m.USER, validate=True)
    def put(self, user_id):
        """Updates user with given user id by json data"""
        return m.update_user(request.get_json(), user_id)

    def delete(self, user_id):
        """Deletes user with given user id"""
        return m.delete_user(user_id)


@ns.route("/movies")
class Movies(Resource):
    def get(self):
        """Returns list of all movies existing in database"""
        return m.movies_list()

    @api.expect(m.MOVIE, validate=True)
    def post(self):
        """Creates movie with passed json data"""
        return m.create_movie(request.get_json())


@ns.route("/movies/<int:movie_id>")
class MoviesOperations(Resource):
    def get(self, movie_id):
        """Returns movie found by passed movie id"""
        return m.get_movie(movie_id)

    @api.expect(m.MOVIE, validate=True)
    def put(self, movie_id):
        """Updates movie with given movie id by passed json data"""
        return m.update_movie(request.get_json(), movie_id)

    def delete(self, movie_id):
        """Deletes movie with given movie id"""
        return m.delete_movie(movie_id)


@ns.route("/ratings")
class Ratings(Resource):
    def get(self):
        """Returns list of all ratings existing in database"""
        return m.ratings_list()

    @api.expect(m.RATING, validate=True)
    def post(self):
        """Creates rating with passed json data"""
        return m.create_rating(request.get_json())


@ns.route("/ratings/<int:movie_id>")
class MovieRatings(Resource):
    def get(self, movie_id):
        """Returns list of all ratings for movie with given movie id"""
        return m.movieratings_list(movie_id)


@ns.route("/ratings/<int:movie_id>/<int:user_id>")
class RatingsOperations(Resource):
    def get(self, movie_id, user_id):
        """Returns rating with given user and movie ids"""
        return m.get_rating(movie_id, user_id)

    @api.expect(m.RATING, validate=True)
    def put(self, movie_id, user_id):
        """Updates rating with given user and movie ids"""
        return m.update_rating(movie_id, user_id, request.get_json())

    def delete(self, movie_id, user_id):
        """Deletes rating with given user and movie ids"""
        return m.delete_rating(movie_id, user_id)
