import logging

import pytest

from src.AvatarServer.server.config import Config
from src.AvatarServer.server.http_handler import HTTPHandler
from src.AvatarServer.Avatar.avatar import Avatar
from src.AvatarServer.AvatarProcessor.WCR_caller import WCRCaller
from PIL import Image


class AvatarProcessorForTest:
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

    async def infer(self, image: Image) -> Avatar:
        result = Avatar("1", "1", "1", "1")
        return result


@pytest.fixture
def avatar_processor_for_test(config_for_test) -> AvatarProcessorForTest:
    logger = logging.getLogger(__file__)
    return AvatarProcessorForTest(
        logger=logger,
        config=config_for_test,
    )


@pytest.fixture
def test_http_handler(config_for_test: Config, avatar_processor_for_test: AvatarProcessorForTest):
    logger = logging.getLogger(__name__)
    return HTTPHandler(
        logger=logger,
        config=config_for_test,
        processor=avatar_processor_for_test
    )
