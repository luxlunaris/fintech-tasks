import os
from time import time

from flask import Response, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from .forms import ClientForm, PhotoForm
from .models import add_client, change_path, clients, remove_client
from .wsgi import app

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["UPLOAD_FOLDER"] = "server/static/"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/")
def index() -> str:
    return render_template("index.html", clients=clients)


@app.route("/add", methods=["GET", "POST"])
def add() -> Response:
    form = ClientForm()
    if form.validate_on_submit():
        add_client(form.name.data, form.phone_num.data, form.e_mail.data)
        return redirect(url_for("index"))
    return render_template("client.html", title="Add client", form=form)


@app.route("/photo/<client_id>", methods=["GET", "POST"])
def change_photo(client_id) -> Response:
    form = PhotoForm()
    if request.method == "POST" and form.validate_on_submit():
        if clients[client_id].photo != "no_photo.jpg":
            os.remove(
                os.path.join(app.config["UPLOAD_FOLDER"], clients[client_id].photo)
            )
        f = form.photo.data
        filename = secure_filename(f.filename)
        postfix = str(int(time())) + client_id + filename[filename.rfind(".") :]
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], postfix))
        change_path(client_id, postfix)
        return redirect(url_for("index"))
    return render_template("change_photo.html", title="Change client photo", form=form)


@app.route("/remove/<client_id>")
def remove(client_id: str) -> Response:
    remove_client(client_id)
    return redirect(url_for("index"))
