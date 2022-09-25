import logging
from aiohttp import web
from .httpHandler import get_routes


class HTTPServer:
    def __init__(
        self,
        logger: logging.Logger
    ) -> None:
        self.logger = logger
        self.app = web.Application()
        self.routes = get_routes()
        self.app.add_routes(self.routes)

    def run(
        self,
    ) -> None:
        self.logger.info(f"server start! routing info: {self.routes}")
        web.run_app(self.app)
