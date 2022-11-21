import json
import asyncio
import urllib
from typing import Dict
from aiohttp import streams
from aiohttp import test_utils
from aiohttp import web


class TempProtocol(asyncio.BaseProtocol):
    def __init__(self):
        self._reading_paused = False


def _make_mocked_request_x_www_form_urlencoded(obj: Dict[str, str], request_path: str) -> web.Request:
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


def _make_mocked_request_json(obj: Dict[str, str], request_path: str) -> web.Request:
    reader = streams.StreamReader(protocol=TempProtocol(), limit=10000)

    bdata = bytes(
        json.dumps(obj),
        encoding="utf-8",
    )
    reader.feed_data(bdata)
    reader.feed_eof()
    return test_utils.make_mocked_request(
        method="POST",
        headers={"Content-Type": "application/json"},
        path=request_path,
        payload=reader,
    )
