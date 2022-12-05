import logging
from dataclasses import asdict
from http import HTTPStatus

from aiohttp import web
import aiohttp

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
            web.post('/avatar_image', self.avatar_image_handler),
            web.post('/character_look_data', self.character_look_data_handler),
            web.post('/icon', self.icon_handler)
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
    
    async def avatar_image_handler(self, request: web.Request):
        post = await request.json()
        avatar_dict = post.get("avatar")
        avatar = Avatar()
        for k, v in avatar_dict.items():
            if not hasattr(avatar, k):
                raise Exception("attribute not in avatar")
            setattr(avatar, k, v)
        try:
            image_str = await self.processor.caller.get_image(avatar=avatar)
            return web.Response(text=image_str)
        except web.HTTPBadRequest as e:
            raise web.HTTPBadRequest(text=e.text)
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
                except aiohttp.ClientConnectionError as err:
                    raise web.HTTPGatewayTimeout(
                        body=f"Gateway Timeout Eror 504: {str(err)}"
                    )
                except Exception:
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

    async def icon_handler(self, request: web.Request):
        post = await request.json()
        icon_code = post.get("icon")
        try:
            return web.Response(
                text=await self.processor.get_icon(icon_code),
                status=HTTPStatus.OK
            )
        except Exception as err:
            raise web.HTTPInternalServerError(
                body=f"Internal Server Error 500: {str(err)}"
            )
