import base64
import io
import logging
from http import HTTPStatus

from aiohttp import web
from PIL import Image

from ..ImageProcessor.image_processor import ImageProcessor
from ..server.config import Config


class HTTPHandler:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
    ):
        self.logger = logger
        self.processor = ImageProcessor(
            logger=self.logger,
            config=config,
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
#        a=request.read()
#        print(a)
#        print(type(a))
        post = await request.post() 
#       print(post)
        bs64 = post.get("bs64")
        image_data = base64.b64decode(bs64)
        image = Image.open(io.BytesIO(image_data))
        result = await self.processor.infer(
            image=image
        )
        return web.json_response(result.to_array())
