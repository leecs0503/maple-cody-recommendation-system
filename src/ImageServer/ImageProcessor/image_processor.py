from PIL import Image
from .WCR_caller import WCRCaller
from ..Avatar.avatar import Avatar


class ImageProcessor:
    def __init__(
        self,
        wcr_server_host: str,
        wcr_server_protocol: str,
        wcr_server_port: int,
        retry_num: int,
        timeout: float,
        backoff: float,
    ):
        self.caller = WCRCaller(
            wcr_server_host=wcr_server_host,
            wcr_server_protocol=wcr_server_protocol,
            wcr_server_port=wcr_server_port,
            retry_num=retry_num,
            timeout=timeout,
            backoff=backoff,
        )

    async def infer(self, input_image: Image) -> Avatar:
        # TODO: implement
        result = Avatar("1", "1", "1", "1")
        return result
