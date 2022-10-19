from src.AvatarServer.util.item_manager import ItemManager
from src.AvatarServer.AvatarProcessor.avatar_processor import AvatarProcessor, PackedCharacterInfo
from src.AvatarServer.AvatarProcessor.WCR_caller import WCRCaller
from src.AvatarServer.server.config import Config
from src.AvatarServer.Avatar.avatar import Avatar
from typing import Optional
import json
import pytest
import logging
import os


class CallerForTest(WCRCaller):
    def __init__(*args, **kwargs):
        pass

    async def get_base_wz(self):
        return {}

    async def get_image(self, avatar: Avatar, ActionQuery: Optional[str] = None):
        return None


@pytest.fixture
def caller_for_test() -> CallerForTest:
    return CallerForTest()


@pytest.fixture
def avatar_processor_for_test(config_for_test: Config, caller_for_test: CallerForTest) -> AvatarProcessor:

    # FIXME: validate 로직 제거 예정
    async def tmp(*args, **kwargs):
        pass
    ItemManager.validate = tmp
    return AvatarProcessor(
        logger=logging.getLogger(__file__),
        config=config_for_test,
        caller=caller_for_test,
    )


def test_infer(avatar_processor_for_test: AvatarProcessor):
    cwd = os.path.dirname(__file__)
    json_path = os.path.join(cwd, 'testdata', 'packed_info.json')

    with open(json_path, 'r') as file:
        data: dict = json.load(file)

    is_not_fail = True
    faile_set = set()
    for user_name, user_data in data.items():
        expected_return_data = PackedCharacterInfo()
        for k, v in user_data.items():
            if k == "str":
                continue
            setattr(expected_return_data, k, v)

        packed_character_look = user_data["str"]
        return_data = avatar_processor_for_test.infer(packed_character_look=packed_character_look)

        # for printing
        for k, v in user_data.items():
            if k == "str":
                continue
            v1 = getattr(return_data, k)
            v2 = getattr(expected_return_data, k)
            if v2 != -1 and v1 != v2:
                print(f"!! {user_name}: {k} is different ({v1} <-> {v2}).")
                is_not_fail = False
                faile_set.add(user_name)

    assert is_not_fail, f"fail list: {faile_set}"

@pytest.mark.asyncio
def test_process_image():
    # TODO: implement
    pass
