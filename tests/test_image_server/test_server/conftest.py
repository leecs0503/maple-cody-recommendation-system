import logging

import pytest

from src.ImageServer.server.config import Config
from src.ImageServer.server.http_handler import HTTPHandler

"""
mocking

class test_for_ImageProcessor:
    def __init__(
        self,
        logger: logging.Logger,
    ):
        self.logger = logger

    async def infer(self,) -> Avatar:
        result = Avatar("1", "1", "1", "1")
        return result



@pytest.fixture
def image_processor(config_for_test: Config):
    logger = logging.getLogger(__name__)
    return test_for_ImageProcessor(
        logger=logger,
        config=config_for_test,
    )
"""


@pytest.fixture
def http_handler(config_for_test: Config):
    logger = logging.getLogger(__name__)

    return HTTPHandler(
        logger=logger,
        config=config_for_test,
    )
