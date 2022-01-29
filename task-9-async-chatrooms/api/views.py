import asyncio
from datetime import datetime

import aiohttp_jinja2
import aioredis
from aiohttp import WSMsgType, web

from .models import (
    chats,
    get_last_messages,
    get_random_name,
    reader,
    save_message,
    valid_name,
)
from .settings import log


async def create_chat(request):
    """
    ---
    description: This endpoint allows you to create new chat room.
    tags:
      - Chat
    consumes:
        - application/json
    parameters:
      - in: body
        name: name
        description: Chat to create.
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
    produces:
      - text/plain
    responses:
      "200":
        description: successful operation
      "400":
        description: invalid name
    """
    data = await request.json()
    if not (len(data.keys()) == 1 and "name" in data and isinstance(data["name"], str)):
        return web.Response(text="Invalid json", status=400)
    name, engine = data["name"], request.app["db"]
    if await valid_name(name, engine):
        return web.Response(text="Chat already exists", status=400)
    async with engine.acquire() as conn:
        await conn.execute(chats.insert().values(name=name))
    return web.Response(text="Chat successfully created", status=201)


async def delete_chat(request):
    """
    ---
    description: This endpoint allows you to delete chat room.
    tags:
    - Chat
    parameters:
      - in: path
        name: name
        schema:
          type: string
          required: true
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation
        "400":
            description: invalid name
    """
    name, engine = request.match_info["name"], request.app["db"]
    if not await valid_name(name, engine):
        return web.Response(text="No such chat", status=404)
    async with engine.acquire() as conn:
        await conn.execute(chats.delete().where(chats.c.name == name))
    return web.Response(text="Chat successfully deleted", status=200)


@aiohttp_jinja2.template("index.html")
async def index(request):
    chatlist = []
    async with request.app["db"].acquire() as conn:
        async for row in conn.execute(chats.select().order_by("name")):
            chatlist.append(row.name)
    return {"chats": chatlist}


async def chat(request):
    channel = request.match_info["name"]
    if not await valid_name(channel, request.app["db"]):
        return web.Response(text="No such chat", status=404)

    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        return aiohttp_jinja2.render_template("chat.html", request, {})
    await ws_current.prepare(request)

    msgs = await get_last_messages(channel, request.app["db"])
    name = get_random_name()

    pub = await aioredis.create_redis(("redis", 6379), db=1, encoding="utf-8")
    sub = await aioredis.create_redis(("redis", 6379), db=1, encoding="utf-8")
    res = await sub.subscribe(channel)
    ch = res[0]

    await ws_current.send_json({"action": "connect", "name": name, "msgs": msgs})
    log.info("%s: %s joined.", channel, name)
    await pub.publish(channel, f"({datetime.now().strftime('%H:%M')}) {name} joined")

    haste_errors = (
        asyncio.TimeoutError,
        RuntimeError,
        aioredis.errors.ChannelClosedError,
    )

    while True:
        while True:
            try:
                await asyncio.wait_for(reader(ch, ws_current), timeout=0.0001)
            except haste_errors:
                break
        while True:
            try:
                msg = await asyncio.wait_for(ws_current.receive(), timeout=0.0001)
                if msg.type == WSMsgType.text:
                    await pub.publish(channel, msg.data)
                    await save_message(msg.data, channel, request.app["db"])
            except haste_errors:
                break
        if ws_current.closed:
            log.info("%s: %s disconnected.", channel, name)
            await pub.publish(
                channel, f"({datetime.now().strftime('%H:%M')}) {name} disconnected"
            )
            await sub.unsubscribe(f"channel:{channel}")
            sub.close()
            pub.close()
            break

    return ws_current
