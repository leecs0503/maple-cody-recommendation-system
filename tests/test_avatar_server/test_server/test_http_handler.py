import asyncio
import os
import pytest
from aiohttp.test_utils import make_mocked_request
import json
import urllib

from aiohttp import streams
from src.AvatarServer.server.http_handler import HTTPHandler

import base64
from src.AvatarServer.Avatar.avatar import Avatar
from aiohttp import test_utils


@pytest.mark.asyncio
async def test_http_index_handler(test_http_handler: HTTPHandler):
    request = make_mocked_request("GET", "/")
    result = await test_http_handler.index_handler(request=request)
    assert result.status == 200


@pytest.mark.asyncio
async def test_http_healthcheck_handler(test_http_handler: HTTPHandler):
    request = make_mocked_request("GET", "/healthcheck")
    result = await test_http_handler.helthcheck_handler(request=request)
    assert result.status == 200


class TempProtocol(asyncio.BaseProtocol):
    def __init__(self):
        self._reading_paused = False


@pytest.mark.asyncio
async def test_http_image_handler(test_http_handler: HTTPHandler):
    base_uri = os.path.dirname(__file__)
    file_path = os.path.join(base_uri, "data", "test_image.png")
    with open(file_path, "rb") as img:
        base64_bstring = base64.b64encode(img.read())
    reader = streams.StreamReader(protocol=TempProtocol(), limit=10000)
    bdata = bytes(
        urllib.parse.urlencode(
            {
                "bs64": str(base64_bstring, encoding="utf-8"),
            }
        ),
        encoding="utf-8",
    )
    reader.feed_data(bdata)
    reader.feed_eof()
    request = test_utils.make_mocked_request(
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        path="/image",
        payload=reader,
    )

    result = await test_http_handler.image_handler(request=request)
    assert result.text == json.dumps(Avatar("1", "1", "1", "1").to_array())

@pytest.mark.asyncio
async def test_http_image_handler(test_http_handler: HTTPHandler):
    pass

@pytest.mark.asyncio
async def test_packed_character_look_handler(test_http_handler: HTTPHandler):
    request = make_mocked_request("POST", "/packed_character_look", headers={"packed_character_look": ""})