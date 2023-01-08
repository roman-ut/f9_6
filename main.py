import aiohttp_jinja2
import jinja2
from aiohttp import web

from app.forum.routes import setup_routes as setup_forum_routes
from app.settings import config, BASE_DIR
from app.store.database.accessor import PostgresAccessor


def setup_config(application):
    application["config"] = config


def setup_external_libraries(application):
    aiohttp_jinja2.setup(
        application,
        loader=jinja2.FileSystemLoader(f"{BASE_DIR}/templates"),
    )


def setup_accessors(application):
    application["db"] = PostgresAccessor()
    application["db"].setup(application)


# настроим url-пути для доступа к нашему будущему приложению
def setup_routes(application):
    setup_forum_routes(application)


def setup_app(application):
    setup_config(application)
    setup_accessors(application)
    setup_external_libraries(application)
    setup_routes(application)


def init():
    app = web.Application()
    app["sockets"] = []
    setup_app(app)
    return app


if __name__ == "__main__":
    web.run_app(init(), port=config["common"]["port"])  # запускаем наше приложение
