import json
import logging
from functools import cached_property

import os
from .config import Config
from .http_server import HttpServer


class AppRunner:
    def __init__(
        self,
        config: Config,
        logging_path: str
    ) -> None:
        self.config = config
        self.logging_path = logging_path

        self.HttpServer = HttpServer(
            logger=self.logger,
            config=self.config,
        )

    @cached_property
    def logger(self):
        logger = logging.getLogger(__name__)

        formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s")

        os.makedirs("logs", exist_ok=True)

        file_handler = logging.FileHandler(self.logging_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)

        return logger

    def run(self) -> None:
        self.logger.info(f"now config: {json.dumps(self.config.to_json())}")

        self.logger.info("start HttpServer")
        self.HttpServer.run()
