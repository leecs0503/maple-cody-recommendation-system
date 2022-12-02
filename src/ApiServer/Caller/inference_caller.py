import asyncio
import logging

import aiohttp
from aiohttp import web


class InferenceCaller:
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
        self.server_host = server_host
        self.server_protocol = server_protocol
        self.server_port = server_port
        self.retry_num = retry_num
        self.session = aiohttp.ClientSession()
        self.timeout = timeout
        self.backoff = backoff

    async def exponential_backoff(self, step: int):
        # https://en.wikipedia.org/wiki/Exponential_backoff
        delay = self.backoff * (2**step)
        await asyncio.sleep(delay)

    async def infer(
        self,
        gender: str,
        item_parts: str,
        b64_character_look: str,
    ):
        url = f"{self.server_protocol}://{self.server_host}:{self.server_port}/{item_parts}"
        retry_num = self.retry_num if self.retry_num >= 0 else 1000000000
        json_data = {
            "gender": gender,
            "parts": item_parts,
            "input_data": b64_character_look
        }

        for step in range(retry_num):
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=json_data, ssl=False) as resp:
                    if resp.status == 200:
                        return await resp.text()  # 아이템 코드를 string의 형태로 리턴해줄 것이라는 기대
                    elif resp.status == 400:
                        raise web.HTTPBadRequest(text=await resp.text())
            await self.exponential_backoff(step)

        raise Exception("err: get_image")
