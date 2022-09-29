import asyncio

from dataclasses import dataclass
import io
import os
import sys
import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request
import json
from multidict import MultiDict

from src.ImageServer.server.http_handler import HTTPHandler
from tests.test_image_server.test_server.conftest import test_for_ImageProcessor

from PIL import Image
import base64
from src.ImageServer.Avatar.avatar import Avatar
from aiohttp import test_utils

@pytest.mark.asyncio
async def test_http_index_handler(http_handler: HTTPHandler):
    request = make_mocked_request('GET', '/')
    result = await http_handler.index_handler(request=request)
    assert result.status == 200


@pytest.mark.asyncio
async def test_http_healthcheck_handler(http_handler: HTTPHandler):
    request = make_mocked_request('GET', '/healthcheck')
    result = await http_handler.helthcheck_handler(request=request)
    assert result.status == 200


@pytest.mark.asyncio
async def test_http_image_handler(http_handler: HTTPHandler):
    base_uri = os.path.dirname(__file__)
    file_path = os.path.join(base_uri, '.data', 'test_image.png')
    with open(file_path, 'rb') as img:
        base64_string = base64.b64encode(img.read())

    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8080)

    request = test_utils.make_mocked_request(
        method="post",
        path="/image",
        writer ={
            "bs64": str(base64_string, 'utf-8'),
        },
        payload=reader
    )
#    print(type(request))
    result = await http_handler.image_handler(request=request)
    assert result.text == json.dumps(Avatar("1", "1", "1", "1").to_array())








'''
class TEST():
    def __init__(self):
        base_uri = os.path.dirname(__file__)
        file_path = os.path.join(base_uri, '.data', 'test_image.png')
        with open(file_path, 'rb') as img:
            base64_string = base64.b64encode(img.read())
        self.response = TESTFORGET(base64_string)
    
    async def post(self):
        return self.response

class TESTFORGET:
    def __init__(self, data):
        self.data=data
    def get(self,key):
        return self.data

@pytest.mark.asyncio
async def test(http_handler: HTTPHandler):
    request=TEST()
    res = await http_handler.image_handler(request=request)

    assert res.text == json.dumps(Avatar("1","1","1","1").to_array())

'''


