import logging
from http import HTTPStatus

from aiohttp import web


class HTTPHandler:
    def __init__(
        self,
        logger: logging.Logger,
    ):
        self.logger = logger

    def get_routes(self):
        return [
            web.get("/", self.index_handler),
            web.get("/healthcheck", self.healthcheck_handler)
        ]

    async def index_handler(self, request: web.Request):
        """ """
        return web.Response(body="-", status=HTTPStatus.OK)

    async def healthcheck_handler(self, request: web.Request):
        """ """
        return web.Response(body="200 OK", status=HTTPStatus.OK)


