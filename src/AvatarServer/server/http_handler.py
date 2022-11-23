import logging
from dataclasses import asdict
from http import HTTPStatus

from aiohttp import web

from ..Avatar.avatar import Avatar
from ..AvatarProcessor.avatar_processor import AvatarProcessor, LookStringVersionException
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
            web.post('/packed_character_look', self.packed_character_look_handler),
            web.post('/character_look_data', self.character_look_data_handler)
        ]

    async def index_handler(self, request: web.Request):
        """ """
        return web.Response(body="-", status=HTTPStatus.OK)

    async def healthcheck_handler(self, request: web.Request):
        """ """
        return web.Response(body="200 OK", status=HTTPStatus.OK)

    async def packed_character_look_handler(self, request: web.Request):
        post = await request.json()
        packed_character_look = post.get("packed_character_look")
        try:
            packed_character_info = self.processor.infer(packed_character_look)
            avatar = packed_character_info.get_avatar()
            result = asdict(avatar)
            return web.json_response(result)
        except LookStringVersionException as err:
            raise web.HTTPBadRequest(
                body=f"Bad Request Error 400: {str(err)}"
            )
        except Exception as err:
            raise web.HTTPInternalServerError(
                body=f"Internal Server Error 500: {str(err)}"
            )
    async def character_look_data_handler(self, request: web.Request):
        post = await request.json()
        packed_character_look = post.get("packed_character_look")
        try:
            packed_character_info = self.processor.infer(packed_character_look)
            avatar = packed_character_info.get_avatar()
            avatar_dict = asdict(avatar)
            result = {}
            for item_type, item_code in avatar_dict.items():
                result[item_type] = item_code
                if item_type == "gender":
                    continue
                setattr(avatar, item_type, "0")
                try:
                    result[f"{item_type}_image"] = await self.processor.process_image(avatar, False)
                except:
                    result[f"{item_type}_image"] = ""
                setattr(avatar, item_type, item_code)
            return web.json_response(result)
        except LookStringVersionException as err:
            raise web.HTTPBadRequest(
                body=f"Bad Request Error 400: {str(err)}"
            )
        except Exception as err:
            raise web.HTTPInternalServerError(
                body=f"Internal Server Error 500: {str(err)}"
            )
