import logging
from functools import cached_property

import os
from .http_server import HTTPServer
from ..Config.config import Config


class AppRunner:
    def __init__(
        self,
        config: Config,
    ) -> None:
        self.config = config
        self.HTTPServer = HTTPServer(
            config=self.config,
            logger=self.logger,
        )

    @cached_property
    def logger(self):
        logger = logging.getLogger(__name__)

        formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s")
        if not os.path.exists('logs'):
            os.makedirs("logs")
        file_handler = logging.FileHandler("logs/app_runner_log.log")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)

        return logger

    def run(self) -> None:
        self.logger.info("start HTTPServer")
        self.HTTPServer.run()
