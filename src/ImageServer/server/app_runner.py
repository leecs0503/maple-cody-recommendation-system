import json
import logging
from functools import cached_property

import os
from .config import Config
from .http_server import HTTPServer


class AppRunner:
    def __init__(
        self,
        wcr_server_host: str,
        wcr_server_port: int,
        wcr_server_protocol: str,
        base_wz_code_path: str,
        wcr_caller_retry_num: int,
        wcr_caller_timeout: float,
        wcr_caller_backoff: float,
    ) -> None:
        self.config = Config(
            wcr_server_host=wcr_server_host,
            wcr_server_port=wcr_server_port,
            wcr_server_protocol=wcr_server_protocol,
            base_wz_code_path=base_wz_code_path,
            wcr_caller_retry_num=wcr_caller_retry_num,
            wcr_caller_timeout=wcr_caller_timeout,
            wcr_caller_backoff=wcr_caller_backoff,
        )
        self.HTTPServer = HTTPServer(
            logger=self.logger,
            config=self.config,
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
        self.logger.info(f"now config: {json.dumps(self.config.to_json())}")

        self.logger.info("start loading base_wz")
        self._load_base_wz()
        self.item_manager.read(self.base_wz)
        # TODO : HTTPServer에 itemManager 넘겨주기
        self.logger.info("complete loading base_wz")

        self.logger.info("start HTTPServer")
        self.HTTPServer.run()
