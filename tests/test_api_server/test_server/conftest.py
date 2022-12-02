import logging

import pytest

from src.ApiServer.server.config import Config
from src.ApiServer.server.http_handler import HttpHandler
from typing import Dict

class AvatarCallerForTest:
    def __init__(self):
        pass

    async def get_character_look_data(self, encrypted_character_look: str):
        return None

    async def get_avatar_image(self, avatar_dict: Dict[str, str]):
        return None


class InferenceCallerForTest:
    def __init__(self):
        pass

    async def infer(
        self,
        gender: str,
        item_parts: str,
        b64_character_look: str,
    ):
        return None

@pytest.fixture
def test_http_handler(config_for_test: Config):
    logger = logging.getLogger(__name__)
    http_handler = HttpHandler(
        logger=logger,
        config=config_for_test,
        avatar_caller=AvatarCallerForTest(),
        inference_caller=InferenceCallerForTest(),
    )
    return http_handler
