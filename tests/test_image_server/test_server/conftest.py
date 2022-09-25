import logging

import pytest

from src.ImageServer.server.config import Config
from src.ImageServer.server.http_handler import HTTPHandler


@pytest.fixture
def http_handler(config_for_test: Config):
    logger = logging.getLogger(__name__)
    
    return HTTPHandler(
        logger=logger,
        config=config_for_test,
    )