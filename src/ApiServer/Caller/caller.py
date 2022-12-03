import asyncio
import logging

import aiohttp
from aiohttp import web
from http import HTTPStatus


class Caller:
    def __init__(
        self,
        logger: logging.Logger,
        server_host: str,
        server_protocol: str,
        server_port: int,
        retry_num: int,
        timeout: float,
        backoff: float,
    ):
        self.logger = logger
        self.server_host = server_host
        self.server_protocol = server_protocol
        self.server_port = server_port
        self.retry_num = retry_num
        self.timeout = timeout
        self.backoff = backoff

    async def exponential_backoff(self, step: int):
        # https://en.wikipedia.org/wiki/Exponential_backoff
        delay = self.backoff * (2**step)
        await asyncio.sleep(delay)

    async def request(
        self,
        route_path: str,
        **kwargs,
    ):
        url = f"{self.server_protocol}://{self.server_host}:{self.server_port}/{route_path}"
        retry_num = self.retry_num if self.retry_num >= 0 else 1000000000

        # TODO: keep alive 사용

        for step in range(retry_num):
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=kwargs, ssl=False) as resp:
                    if resp.status == HTTPStatus.OK:
                        return await resp.json()
                    elif resp.status == HTTPStatus.BAD_REQUEST:
                        raise web.HTTPBadRequest(text=await resp.text())
            await self.exponential_backoff(step)

        raise Exception(f"err: {route_path}")
