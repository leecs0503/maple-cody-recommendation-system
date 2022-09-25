from aiohttp import web
import base64

from http import HTTPStatus
from PIL import Image
import io
from ..ImageProcessor.image_processor import ImageProcessor


class HTTPHandler:
    def __init__(
        self,
        wcr_server_host: str,
        wcr_server_port: int,
        wcr_server_protocol: str,
        retry_num: int = -1,
        timeout: float = 2,
        backoff: float = 1,
    ):
        self.processor = ImageProcessor(
            wcr_server_host=wcr_server_host,
            wcr_server_port=wcr_server_port,
            wcr_server_protocol=wcr_server_protocol,
            retry_num=retry_num,
            timeout=timeout,
            backoff=backoff,
        )

    def get_routes(self):
        return [
            web.get('/', self.index_handler),
            web.get('/healthcheck', self.helthcheck_handler),
            web.post('/image', self.image_handler),
        ]

    async def index_handler(self, request: web.Request):
        """

        """
        return web.Response(body="-", status=HTTPStatus.OK)

    async def helthcheck_handler(self, request: web.Request):
        """

        """
        return web.Response(body="200 OK", status=HTTPStatus.OK)

    async def image_handler(self, request: web.Request):
        """

        """
        post = await request.post()
        bs64 = post.get("bs64")
        image_data = base64.b64decode(bs64)
        image = Image.open(io.Bytesio(image_data))
        result = await self.processor.infer(
            image=image
        )

        return web.json_response(result)
