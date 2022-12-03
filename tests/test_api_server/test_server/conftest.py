import logging

import pytest
import json
import os

from src.ApiServer.server.config import Config
from src.ApiServer.server.http_handler import HttpHandler


class CallerForTest:
    def __init__(self):
        cwd = os.path.dirname(__file__)
        json_path = os.path.join(cwd, 'test_data', 'test_recommend_data.json')
        with open(json_path, 'rt') as file:
            self.data = json.load(file)

    async def request(
        self,
        route_path: str,
        **kwargs,
    ):
        if route_path == "/character_look_data":
            return self.data["get_character_look_data"]

        if route_path == "/avatar_image":
            return json.dumps(kwargs)

        if "parts" in kwargs and f"/{kwargs['parts']}" == route_path:
            return kwargs["parts"]

        raise Exception("invalid request")


@pytest.fixture
def test_http_handler(config_for_test: Config):
    logger = logging.getLogger(__name__)
    http_handler = HttpHandler(
        logger=logger,
        config=config_for_test,
        avatar_caller=CallerForTest(),
        inference_caller=CallerForTest(),
    )
    return http_handler
