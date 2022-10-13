import asyncio
import logging
from typing import Optional

import aiohttp

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

    async def get_image(self, avatar: Avatar, ActionQuery: Optional[str] = None):
        retry_num = self.retry_num if self.retry_num >= 0 else 1000000000
        params = avatar.to_param()
        if ActionQuery is not None:
            params.append(("actionName", ActionQuery))
        for step in range(retry_num):
            url = f"{self.wcr_server_protocol}://{self.wcr_server_host}:{self.wcr_server_port}/image"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, ssl=False) as resp:
                    if resp.status == 200:
                        return await resp.text()
            await self.exponential_backoff(step)
