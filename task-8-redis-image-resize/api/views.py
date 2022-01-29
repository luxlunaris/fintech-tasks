from flask import request
from flask_restplus import Resource, fields

from .models import delete_image, get_image, upload_image
from .wsgi import api

ns = api.namespace("images", description="Operations with images")


IMAGE_UPLOAD = api.model(
    "Image",
    {"image": fields.String, "size_X": fields.Integer, "size_Y": fields.Integer},
)


@ns.route("/")
class Images(Resource):
    @api.expect(IMAGE_UPLOAD, validate=True)
    def post(self):
        print(request.get_json())
        """Uploads image to server and returns url"""
        return upload_image(request.get_json())


@ns.route("/<url>")
class ImageOperations(Resource):
    def get(self, url):
        """Returns processed image by url"""
        return get_image(url)

    def delete(self, url):
        """Deletes image by url"""
        return delete_image(url)
