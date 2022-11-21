import logging

import pytest

from src.ApiServer.server.config import Config
from src.ApiServer.server.http_handler import HttpHandler


@pytest.fixture
def test_http_handler(config_for_test: Config):
    logger = logging.getLogger(__name__)
    http_handler = HttpHandler(
        logger=logger,
        config=config_for_test,
    )
    return http_handler
