import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiopg.sa import create_engine

from .settings import BASE_DIR, config
from .views import chat, create_chat, delete_chat, index


def create_app():
    app = web.Application()
    app.router.add_static("/static/", path=BASE_DIR / "api" / "static", name="static")
    app["config"] = config
    app.router.add_route("GET", "/", index, name="list")
    app.router.add_route("POST", "/", create_chat, name="create")
    app.router.add_route("GET", "/{name}", chat, name="join")
    app.router.add_route("DELETE", "/{name}", delete_chat, name="delete")
    app.on_startup.append(init_pg)
    app.on_shutdown.append(close_pg)
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader("api", "templates"))
    return app


async def init_pg(app):
    conf = app["config"]["postgres"]
    engine = await create_engine(
        database=conf["database"],
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
    )
    app["db"] = engine


async def close_pg(app):
    app["db"].close()
    await app["db"].wait_closed()
