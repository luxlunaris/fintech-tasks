from random import uniform

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Currency, User, User_Currency

url = "postgresql+psycopg2://Cryptomanager:2hard2pass@postgres:5432/Cryptocurrencies"
engine = create_engine(url)
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    sess = Session()
    names = [
        "Memecoin",
        "Bitcoin",
        "Mackerelcoin",
        "Cheburcoin",
        "ZCash",
        "Dreamcoin",
        "UberChain",
        "Pay4me",
        "FooCoin",
        "BarCoin",
        "BazCoin",
        "UCoin",
        "CoinHasNoName",
        "MinedInDepth",
        "ForgedInVideocard",
    ]
    currency_list = []
    for i in range(15):
        b = round(uniform(1, 100), 2)
        s = round(b * 0.75, 2)
        currency_list.append(
            Currency(id=i, name=names[i], price_to_buy=b, price_to_sell=s)
        )
    for currency in currency_list:
        sess.add(currency)
    sess.commit()
    sess.close()
