import os

from flask import Response, abort, flash, redirect, render_template, request, url_for

from db import Session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from .forms import LoginForm, RegistrationForm, TransactionForm
from .models import Currency, User, create_user, User_Currency
from .wsgi import app

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    s = Session()
    user = s.query(User).filter_by(id=user_id).first()
    s.close()
    return user


@app.route("/")
def index() -> str:
    s = Session()
    currencies = s.query(Currency).all()
    wallet = (
        []
        if not current_user.is_authenticated
        else s.query(User_Currency)
        .filter_by(user_id=current_user.id)
        .order_by(User_Currency.currency_id)
    )
    s.close()
    return render_template(
        "index.html", user=current_user, currencies=currencies, wallet=wallet
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        s = Session()
        create_user(form.username.data, form.email.data, form.password.data, s)
        s.close()
        flash("Thank you for registration")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        login_user(form.user)
        flash("Logged in successfully.")
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/maketrans/<cid>", methods=["GET", "POST"])
@login_required
def maketrans(cid):
    s = Session()
    name = s.query(Currency).filter_by(id=cid).first().name
    s.close()
    form = TransactionForm()
    form.uid = current_user.id
    form.cid = cid
    if request.method == "POST" and form.validate_on_submit():
        s = Session()
        if form.buy_curr.data:
            s.query(User_Currency).filter_by(
                user_id=current_user.id, currency_id=cid
            ).update(
                {"currency_val": User_Currency.currency_val + form.value_to_buy.data}
            )
            s.query(User).filter_by(id=current_user.id).update(
                {
                    "money": User.money
                    - form.currency.price_to_buy * form.value_to_buy.data
                }
            )
        else:
            s.query(User_Currency).filter_by(
                user_id=current_user.id, currency_id=cid
            ).update(
                {"currency_val": User_Currency.currency_val - form.value_to_sell.data}
            )
            s.query(User).filter_by(id=current_user.id).update(
                {
                    "money": User.money
                    + form.currency.price_to_sell * form.value_to_sell.data
                }
            )
        s.commit()
        s.close()
        return redirect(url_for("index"))
    return render_template("trans.html", form=form, name=name)
