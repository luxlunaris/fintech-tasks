import json
from api.app import create_app
import pytest
from uuid import uuid4


async def test_simple(test_client):
    client = await test_client(create_app())

    get1 = await client.get("/")
    text1 = await get1.text()
    assert "List of chats" in text1

    get2 = await client.get("/English")
    text2 = await get2.text()
    assert "Welcome to chat" in text2


async def test_create(test_client):
    client = await test_client(create_app())

    post1 = await client.post("/", data=json.dumps({"name": uuid4().hex[:8]}))
    text1 = await post1.text()
    assert "Chat successfully created" in text1

    post2 = await client.post("/", data=json.dumps(dict(name="Chinese")))
    text2 = await post2.text()
    assert "Chat already exists" in text2

    post3 = await client.post("/", data=json.dumps(dict(not_name="string1")))
    text3 = await post3.text()
    assert "Invalid json" in text3


async def test_delete(test_client):
    client = await test_client(create_app())

    delete1 = await client.delete("/Russian")
    text1 = await delete1.text()
    assert "Chat successfully deleted" in text1

    delete2 = await client.delete("/Not_a_chat")
    text2 = await delete2.text()
    assert "No such chat" in text2
