import logging

from aiohttp import web

from ..util.item_manager import ItemManager

from .config import Config
from .http_handler import HTTPHandler


class HTTPServer:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
        item_manager: ItemManager,
    ) -> None:
        self.logger = logger
        self.app = web.Application()
        self.config = config
        self.HTTPHandler = HTTPHandler(
            logger=self.logger,
            config=config,
            item_manager=item_manager,
        )
        self.routes = self.HTTPHandler.get_routes()
        self.app.add_routes(self.routes)

    def run(
        self,
    ) -> None:
        self.logger.info(f"server start! routing info: {self.routes}")
        web.run_app(self.app)
