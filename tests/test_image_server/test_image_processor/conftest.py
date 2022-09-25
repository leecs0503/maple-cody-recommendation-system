import logging

import pytest

from src.ImageServer.ImageProcessor.image_processor import ImageProcessor
from src.ImageServer.server.config import Config


@pytest.fixture
def image_processor(test_config: Config):
    logger = logging.getLogger(__name__)
    return ImageProcessor(
        logger=logger,
        config=test_config,
    )
