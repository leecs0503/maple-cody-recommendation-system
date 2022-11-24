import logging
from http import HTTPStatus
from ..Trainer.trainer import Trainer
from ..Config.config import Config

from aiohttp import web


class HTTPHandler:
    def __init__(
        self,
        config: Config,
        logger: logging.Logger,
    ):
        self.config = config
        self.logger = logger
        self.trainer = Trainer(
            config=config,
            logger=self.logger,
        )

    def get_routes(self):
        return [
            web.get("/", self.index_handler),
            web.get("/healthcheck", self.healthcheck_handler),
            web.post("/train", self.train_handler)
        ]

    async def index_handler(self, request: web.Request):
        """ """
        return web.Response(body="-", status=HTTPStatus.OK)

    async def healthcheck_handler(self, request: web.Request):
        """ """
        return web.Response(body="200 OK", status=HTTPStatus.OK)

    async def train_handler(self, request: web.Request):
        post = await request.json()
        train_data = post.get("train_data")
        self.trainer.load_data(train_data)
        return web.Response(body="-", status=HTTPStatus.OK)
