from datetime import datetime

from sqlalchemy import MetaData, create_engine

from api.models import chats, messages
from api.settings import config

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.drop_all(bind=engine)
    meta.create_all(bind=engine, tables=[chats, messages])


def add_chats(engine):
    conn = engine.connect()
    conn.execute(
        chats.insert(),
        [
            {"name": "Russian"},
            {"name": "English"},
            {"name": "Chinese"},
            {"name": "Japanese"},
            {"name": "French"},
            {"name": "German"},
            {"name": "Polish"},
            {"name": "Swedish"},
            {"name": "Finnish"},
        ],
    )
    conn.execute(
        messages.insert(),
        [
            {
                "chat_name": "Russian",
                "message": f'({datetime.now().strftime("%H:%M")}) Andrew: There is',
                "date": datetime.now(),
            },
            {
                "chat_name": "Russian",
                "message": f'({datetime.now().strftime("%H:%M")}) Andrew: something',
                "date": datetime.now(),
            },
            {
                "chat_name": "Russian",
                "message": f'({datetime.now().strftime("%H:%M")}) Andrew: foo in my bar',
                "date": datetime.now(),
            },
            {
                "chat_name": "Russian",
                "message": f'({datetime.now().strftime("%H:%M")}) Andrew: sample text',
                "date": datetime.now(),
            },
            {
                "chat_name": "Russian",
                "message": f'({datetime.now().strftime("%H:%M")}) Andrew: another message',
                "date": datetime.now(),
            },
        ],
    )
    conn.close()


if __name__ == "__main__":
    db_url = DSN.format(**config["postgres"])
    engine = create_engine(db_url)
    create_tables(engine)
    add_chats(engine)
