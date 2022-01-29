from app.models import User, Currency, User_Currency, create_user, unimmute
from db import Session
import pytest
from uuid import uuid4


def test_create_user():
    s = Session()
    create_user("Alan", "alan@char.com", "bypassed", s)
    q = s.query(User).all()
    s.close()
    assert len(q) == 1
    assert q[0].username == "Alan"


def test_create_currency():
    s = Session()
    currency = Currency(id=1, name="SomeCoin", price_to_buy=10, price_to_sell=9)
    s.add(currency)
    s.commit()
    q = s.query(Currency).all()
    s.close()
    assert len(q) == 1
    assert q[0].name == "SomeCoin"


def test_create_wallet():
    s = Session()
    user = User(
        id=uuid4().hex,
        username="Alan",
        e_mail="idonot@exist.lol",
        password="hashitdummy",
        is_authenticated=False,
        money=1000,
    )
    currency = Currency(id=1, name="SomeCoin", price_to_buy=10, price_to_sell=9)
    s.add(user)
    s.add(currency)
    pocket = User_Currency(
        id=uuid4().hex,
        user_id=user.id,
        currency_id=currency.id,
        currency_name=currency.name,
        currency_val=0,
    )
    s.add(pocket)
    s.commit()
    q = s.query(User_Currency).all()
    s.close()
    assert len(q) == 1
    assert q[0].currency_val == 0


def test_unimmute():
    tup = (1, 2, "a")
    assert unimmute(tup, "b") == (1, 2, "a", "b")
