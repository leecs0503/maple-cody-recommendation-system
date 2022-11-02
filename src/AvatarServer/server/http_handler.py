import base64
import io
import logging
from dataclasses import asdict
from http import HTTPStatus

from aiohttp import web
from PIL import Image

from ..AvatarProcessor.avatar_processor import AvatarProcessor
from ..server.config import Config


class HTTPHandler:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
        processor: AvatarProcessor = None
    ):
        self.logger = logger
        self.processor = AvatarProcessor(
            logger=self.logger,
            config=config,
        ) if processor is None else processor

    def get_routes(self):
        return [
            web.get("/", self.index_handler),
            web.get("/healthcheck", self.healthcheck_handler),
            web.post("/image", self.image_handler),
            web.post('/packed_character_look', self.packed_character_look_handler)
        ]

    async def index_handler(self, request: web.Request):
        """ """
        return web.Response(body="-", status=HTTPStatus.OK)

    async def healthcheck_handler(self, request: web.Request):
        """ """
        return web.Response(body="200 OK", status=HTTPStatus.OK)

    # TODO: deprecated
    async def image_handler(self, request: web.Request):
        """ """
        post = await request.post()
        bs64str = post.get("bs64")
        image_data = base64.b64decode(bs64str)
        image = Image.open(io.BytesIO(image_data))
        result = await self.processor.infer(image=image)
        return web.json_response(result.to_array())

    async def packed_character_look_handler(self, request: web.Request):
        post = await request.post()
        packed_character_look = post.get("packed_character_look")
        try:
            packed_character_info = self.processor.infer(packed_character_look)
            avatar = packed_character_info.get_avatar()
            result = asdict(avatar)
            return web.json_response(result)
        except Exception as err:
            raise web.HTTPInternalServerError(
                body=f"Internal Server Error 500: {str(err)}"
            )