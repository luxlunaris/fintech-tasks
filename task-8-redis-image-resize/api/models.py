import base64
import binascii
import json
from io import BytesIO
from uuid import uuid4

from flask import jsonify
from PIL import Image

import rq
from redis import Redis

r = Redis(host="redis", port=6379, db=0)
q = rq.Queue(connection=r)


def upload_image(data):
    try:
        base64.decodebytes(bytes(data["image"], "utf-8"))
    except binascii.Error:
        return "not base64 string", 400
    if data["size_X"] < 1 or data["size_Y"] < 1:
        return "height and width must be greater than 0", 400
    new_url = uuid4().hex
    r.set(new_url, data["image"])
    job = q.enqueue(resize, args=(data["size_X"], data["size_Y"], new_url))
    return jsonify(
        json.dumps(
            {
                "message": "Your request is being processed",
                "url": f"{new_url}{data['size_X']}x{data['size_Y']}",
            }
        )
    )


def get_image(url):
    if not r.exists(url):
        return "Invalid url. If you got this id as the answer for resizing request - connect again later."
    return jsonify(json.dumps({"image": str(r.get(url), "utf-8")}))


def delete_image(url):
    if not r.exists(url):
        return "Invalid url", 400
    r.delete(url)
    return "Image successfully deleted"


def resize(size_x, size_y, url):
    size = size_x, size_y
    im = Image.open(BytesIO(base64.b64decode(r.get(url)))).convert("RGB")
    im.thumbnail(size, Image.ANTIALIAS)
    buffered = BytesIO()
    im.save(buffered, format="JPEG")
    img_new = base64.b64encode(buffered.getvalue())
    r.set(f"{url}{size_x}x{size_y}", img_new)
