from datetime import datetime

from faker import Faker
from sqlalchemy import Column, Date, ForeignKey, Integer, MetaData, String, Table, desc

meta = MetaData()


chats = Table("chat", meta, Column("name", String(30), primary_key=True))


messages = Table(
    "message",
    meta,
    Column("id", Integer, primary_key=True),
    Column("chat_name", String(30), ForeignKey("chat.name", ondelete="CASCADE")),
    Column("message", String, nullable=False),
    Column("date", Date, nullable=False),
)


def get_random_name():
    fake = Faker()
    return fake.name()


async def save_message(msg, chat_name, engine):
    async with engine.acquire() as conn:
        await conn.execute(
            messages.insert().values(
                chat_name=chat_name, message=msg, date=datetime.now()
            )
        )


async def get_last_messages(chat_name, engine):
    async with engine.acquire() as conn:
        msgsProxy = await conn.execute(
            messages.select()
            .where(messages.c.chat_name == chat_name)
            .order_by(desc("date"))
            .limit(20)
        )
        msgs = []
        async for msg in msgsProxy:
            msgs.append(msg.message)
    return msgs


async def reader(channel, socket):
    msg = await channel.get(encoding="utf-8")
    await socket.send_json({"action": "sent", "msg": msg})


async def valid_name(name, engine):
    async with engine.acquire() as conn:
        chat = await conn.execute(chats.select().where(chats.c.name == name))
        if chat.rowcount != 0:
            return True
    return False
