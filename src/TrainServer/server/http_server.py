import logging

from aiohttp import web

from .http_handler import HTTPHandler


class HTTPServer:
    def __init__(
        self,
        server_host: str,
        server_port: int,
        logger: logging.Logger,
    ) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.logger = logger
        self.app = web.Application()
        self.HTTPHandler = HTTPHandler(logger=self.logger)
        self.routes = self.HTTPHandler.get_routes()
        self.app.add_routes(self.routes)

    def run(
        self,
    ) -> None:
        self.logger.info(f"server start! routing info: {self.routes}")
        web.run_app(
            self.app,
            host=self.server_host,
            port=self.server_port,
        )
