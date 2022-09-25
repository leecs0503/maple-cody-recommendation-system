import logging

from PIL import Image

from ..Avatar.avatar import Avatar
from ..server.config import Config
from .WCR_caller import WCRCaller


class ImageProcessor:
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
