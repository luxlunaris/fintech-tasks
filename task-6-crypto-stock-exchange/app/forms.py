from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from db import Session

from .models import User, unimmute, Currency, User_Currency


class RegistrationForm(FlaskForm):
    def validate(self):
        s = Session()
        user = s.query(User).filter_by(username=self.username.data).first()
        if user:
            self.username.errors = unimmute(
                self.username.errors, "This username is already in use"
            )
            return False
        user = s.query(User).filter_by(e_mail=self.email.data).first()
        if user:
            self.email.errors = unimmute(
                self.email.errors, "This E-mail address is already in use"
            )
            return False
        s.close()
        return True

    username = StringField("Username", validators=[Length(min=4, max=25)])
    email = StringField("Email Address", validators=[Email(), Length(min=6, max=35)])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), EqualTo("confirm", message="Passwords must match")],
    )
    confirm = PasswordField("Repeat Password")
    submit = SubmitField("Registrate me")


class LoginForm(FlaskForm):
    def validate(self):
        s = Session()
        user = s.query(User).filter_by(username=self.username.data).first()
        if not user:
            self.username.errors = unimmute(self.username.errors, "Unknown username")
            return False
        if not user.password == self.password.data:
            self.password.errors = unimmute(self.password.errors, "Invalid password")
            return False
        s.close()
        self.user = user
        return True

    username = StringField("Username", validators=[Length(min=4, max=25)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log me in")


class TransactionForm(FlaskForm):
    def validate(self):
        s = Session()
        buy, sell = self.value_to_buy.data, self.value_to_sell.data
        self.currency = s.query(Currency).filter_by(id=self.cid).first()
        user = s.query(User).filter_by(id=self.uid).first()
        c_wallet = (
            s.query(User_Currency)
            .filter_by(user_id=self.uid, currency_id=self.cid)
            .first()
        )
        if not buy and self.buy_curr.data:
            self.value_to_buy.errors = unimmute(
                self.value_to_buy.errors, "Field is empty"
            )
            return False
        if not sell and self.sell_curr.data:
            self.value_to_sell.errors = unimmute(
                self.value_to_sell.errors, "Field is empty"
            )
            return False
        if buy and self.currency.price_to_buy * buy > user.money:
            self.value_to_buy.errors = unimmute(
                self.value_to_buy.errors, "You cannot afford that"
            )
            return False
        if sell and sell > c_wallet.currency_val:
            self.value_to_sell.errors = unimmute(
                self.value_to_sell.errors, "You don't have enough currency to sell"
            )
            return False
        s.close()
        return True

    value_to_buy = FloatField("Value to buy")
    value_to_sell = FloatField("Value to sell")
    buy_curr = SubmitField("Buy")
    sell_curr = SubmitField("Sell")
    uid = StringField()
    cid = IntegerField()
