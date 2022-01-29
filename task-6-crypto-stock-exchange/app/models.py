from uuid import uuid4

from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", String, primary_key=True)
    username = Column("username", String, unique=True)
    e_mail = Column("e_mail", String, unique=True)
    password = Column("password", String)
    is_authenticated = Column("is_authenticated", Boolean, default=False)
    money = Column("money", Float)

    def __init__(self, id, username, e_mail, password, is_authenticated, money):
        self.id = id
        self.username = username
        self.e_mail = e_mail
        self.password = password
        self.is_authenticated = is_authenticated
        self.money = money

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.is_authenticated

    def get_id(self):
        return self.id


class Currency(Base):
    __tablename__ = "currencies"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, unique=True)
    price_to_buy = Column("price_to_buy", Float)
    price_to_sell = Column("price_to_sell", Float)

    def __init__(self, id, name, price_to_buy, price_to_sell):
        self.id = id
        self.name = name
        self.price_to_buy = price_to_buy
        self.price_to_sell = price_to_sell


class User_Currency(Base):
    __tablename__ = "user_currencies"

    wallet_id = Column("wallet_id", String, primary_key=True)
    user_id = Column("user_id", String)
    currency_id = Column("currency_id", Integer)
    currency_name = Column("currency_name", String)
    currency_val = Column("currency_val", Float)

    def __init__(self, wallet_id, user_id, currency_id, currency_name, currency_val):
        self.wallet_id = wallet_id
        self.user_id = user_id
        self.currency_id = currency_id
        self.currency_name = currency_name
        self.currency_val = currency_val


def create_user(name, email, p_word, session):
    user = User(
        id=uuid4().hex,
        username=name,
        e_mail=email,
        password=p_word,
        is_authenticated=False,
        money=10000,
    )
    session.add(user)
    currencies = session.query(Currency).all()
    for currency in currencies:
        session.add(
            User_Currency(
                wallet_id=uuid4().hex,
                user_id=user.id,
                currency_id=currency.id,
                currency_name=currency.name,
                currency_val=0,
            )
        )
    session.commit()


def unimmute(tup, val):
    tup = list(tup)
    tup.append(val)
    return tuple(tup)
