import logging

from aiohttp import web

from .http_handler import HTTPHandler


class HTTPServer:
    def __init__(
        self,
        logger: logging.Logger,
        wcr_server_host: str,
        wcr_server_port: int,
        wcr_server_protocol: str,
        wcr_caller_retry_num: int = -1,
        wcr_caller_timeout: float = 2,
        wcr_caller_backoff: float = 1,
    ) -> None:
        self.logger = logger
        self.app = web.Application()
        self.HTTPHandler = HTTPHandler(
            logger=self.logger,
            wcr_server_host=wcr_server_host,
            wcr_server_port=wcr_server_port,
            wcr_server_protocol=wcr_server_protocol,
            wcr_caller_retry_num=wcr_caller_retry_num,
            wcr_caller_timeout=wcr_caller_timeout,
            wcr_caller_backoff=wcr_caller_backoff,
        )
        self.routes = self.HTTPHandler.get_routes()
        self.app.add_routes(self.routes)

    def run(
        self,
    ) -> None:
        self.logger.info(f"server start! routing info: {self.routes}")
        web.run_app(self.app)
