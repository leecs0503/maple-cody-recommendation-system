import asyncio
import os
import pytest
from aiohttp.test_utils import make_mocked_request
import json
import urllib

from typing import Dict
from aiohttp import streams
from src.AvatarServer.server.http_handler import HTTPHandler

import base64
from src.AvatarServer.Avatar.avatar import Avatar
from aiohttp import test_utils
from aiohttp import web


@pytest.mark.asyncio
async def test_http_index_handler(test_http_handler: HTTPHandler):
    request = make_mocked_request("GET", "/")
    result = await test_http_handler.index_handler(request=request)
    assert result.status == 200


@pytest.mark.asyncio
async def test_http_healthcheck_handler(test_http_handler: HTTPHandler):
    request = make_mocked_request("GET", "/healthcheck")
    result = await test_http_handler.healthcheck_handler(request=request)
    assert result.status == 200


class TempProtocol(asyncio.BaseProtocol):
    def __init__(self):
        self._reading_paused = False



def _make_mocked_request(obj: Dict[str, str], request_path: str) -> web.Request:
    reader = streams.StreamReader(protocol=TempProtocol(), limit=10000)
    bdata = bytes(
        urllib.parse.urlencode(obj),
        encoding="utf-8",
    )
    reader.feed_data(bdata)
    reader.feed_eof()
    return test_utils.make_mocked_request(
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        path=request_path,
        payload=reader,
    )


@pytest.mark.asyncio
async def test_packed_character_look_handler(test_http_handler: HTTPHandler):
    request = _make_mocked_request(
        obj={
            "packed_character_look": "abc"
        },
        request_path='/packed_character_look'
    )
    result = await test_http_handler.packed_character_look_handler(request=request)
    assert test_http_handler.processor.infer_count == 1
    assert isinstance(result.text, str)