import logging

import pytest

from src.ImageServer.server.config import Config
from src.ImageServer.server.http_handler import HTTPHandler
from src.ImageServer.Avatar.avatar import Avatar
from src.ImageServer.ImageProcessor.WCR_caller import WCRCaller
from PIL import Image

pytest_plugins = 'aiohttp.pytest_plugin'


class test_for_ImageProcessor:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
    ):
        self.logger = logger
        self.caller = WCRCaller(
            logger=self.logger,
            wcr_server_host=config.wcr_server_host,
            wcr_server_protocol=config.wcr_server_protocol,
            wcr_server_port=config.wcr_server_port,
            retry_num=config.wcr_caller_retry_num,
            timeout=config.wcr_caller_timeout,
            backoff=config.wcr_caller_backoff,
        )

    async def infer(self, input_image: Image) -> Avatar:
        # TODO: implement
        result = Avatar("1", "1", "1", "1")
        return result



@pytest.fixture
def test_image_processor(config_for_test: Config):
    logger = logging.getLogger(__name__)
    return test_for_ImageProcessor(
        logger=logger,
        config=config_for_test,
    )


@pytest.fixture
def http_handler(config_for_test: Config):
    logger = logging.getLogger(__name__)

    return HTTPHandler(
        logger=logger,
        config=config_for_test,
    )
