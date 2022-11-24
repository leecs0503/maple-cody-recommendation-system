import logging

from aiohttp import web

from .http_handler import HTTPHandler
from ..Config.config import Config


class HTTPServer:
    def __init__(
        self,
        config: Config,
        logger: logging.Logger,
    ) -> None:
        self.config = config
        self.logger = logger
        self.app = web.Application()
        self.HTTPHandler = HTTPHandler(
            config=config,
            logger=self.logger
        )
        self.routes = self.HTTPHandler.get_routes()
        self.app.add_routes(self.routes)

    def run(
        self,
    ) -> None:
        self.logger.info(f"server start! routing info: {self.routes}")
        web.run_app(
            self.app,
            host=self.config.server_host,
            port=self.config.server_port,
        )
