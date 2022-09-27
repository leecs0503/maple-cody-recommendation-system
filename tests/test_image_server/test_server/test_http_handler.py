import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

from src.ImageServer.server.http_handler import HTTPHandler


def test_http_index_handler(http_handler: HTTPHandler):
    # TODO: implement
    pass


def test_http_healthcheck_handler(http_handler: HTTPHandler):
    # TODO: implement
    pass


@pytest.mark.asyncio
async def test_http_image_handler(http_handler: HTTPHandler):
    # https://docs.aiohttp.org/en/stable/testing.html
    def handler(request):
        assert request.headers.get("token") == "x"
        return web.Response(body=b"data")

    req = make_mocked_request("POST", "/image", headers={"token": "x"})
    resp = handler(req)

    result = await http_handler.image_handler(resp)
    assert result.to_array() == ["1", "1", "1", "1"]

    # TODO: implement
