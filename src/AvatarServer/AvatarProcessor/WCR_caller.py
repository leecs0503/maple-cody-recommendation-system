import asyncio
import json
import logging
from http import HTTPStatus
from typing import Optional

import aiohttp
from aiohttp import web

from ..Avatar.avatar import Avatar


class WCRCaller:
    def __init__(
        self,
        logger: logging.Logger,
        wcr_server_host: str,
        wcr_server_protocol: str,
        wcr_server_port: int,
        retry_num: int,
        timeout: float,
        backoff: float,
    ):
        self.wcr_server_host = wcr_server_host
        self.wcr_server_protocol = wcr_server_protocol
        self.wcr_server_port = wcr_server_port
        self.retry_num = retry_num
        self.session = aiohttp.ClientSession()
        self.timeout = timeout
        self.backoff = backoff

    async def exponential_backoff(self, step: int):
        # https://en.wikipedia.org/wiki/Exponential_backoff
        delay = self.backoff * (2**step)
        await asyncio.sleep(delay)

    async def get_base_wz(self):
        url = f"{self.wcr_server_protocol}://{self.wcr_server_host}:{self.wcr_server_port}/code"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as resp:
                if resp.status == 200:
                    return json.loads(await resp.text())
        raise Exception("err: get_base_wz")

    async def get_avatar_image(self, avatar: Avatar, ActionQuery: Optional[str] = None):
        """ caller의 get image """
        url = f"{self.wcr_server_protocol}://{self.wcr_server_host}:{self.wcr_server_port}/avatar/"
        retry_num = self.retry_num if self.retry_num >= 0 else 1000000000
        params = avatar.to_param()

        # FIXME: temp code
        if ActionQuery is not None:
            params.append(("actionQuery", ActionQuery))

        params.append(("bs", "true"))

        for step in range(retry_num):
            async with aiohttp.ClientSession() as session:
                # TODO: 무기 처리 코드 추가
                async with session.get(url, params=params, ssl=False) as resp:
                    if resp.status == HTTPStatus.OK:
                        return await resp.text()
                    if resp.status == HTTPStatus.BAD_REQUEST:
                        raise web.HTTPBadRequest(text=await resp.text())
            await self.exponential_backoff(step)

        raise Exception("err: get_image")

    async def get_icon(self, item_code: str):
        url = f"{self.wcr_server_protocol}://{self.wcr_server_host}:{self.wcr_server_port}/icon/"
        retry_num = self.retry_num if self.retry_num >= 0 else 1000000000
        params = [
            ("code", item_code),
            ("bs", "true"),
        ]

        for step in range(retry_num):
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, ssl=False) as resp:
                    if resp.status == HTTPStatus.OK:
                        return await resp.text()
                    if resp.status == HTTPStatus.BAD_GATEWAY:
                        raise web.HTTPBadRequest(text=await resp.text())
            await self.exponential_backoff(step)

        raise Exception("err: get_icon")
