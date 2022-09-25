import logging

from PIL import Image

from ..Avatar.avatar import Avatar
from .WCR_caller import WCRCaller


class ImageProcessor:
    def __init__(
        self,
        logger: logging.Logger,
        wcr_server_host: str,
        wcr_server_protocol: str,
        wcr_server_port: int,
        wcr_caller_retry_num: int,
        wcr_caller_timeout: float,
        wcr_caller_backoff: float,
    ):
        self.logger = logger
        self.caller = WCRCaller(
            logger=self.logger,
            wcr_server_host=wcr_server_host,
            wcr_server_protocol=wcr_server_protocol,
            wcr_server_port=wcr_server_port,
            retry_num=wcr_caller_retry_num,
            timeout=wcr_caller_timeout,
            backoff=wcr_caller_backoff,
        )

    async def infer(self, input_image: Image) -> Avatar:
        # TODO: implement
        result = Avatar("1", "1", "1", "1")
        return result
