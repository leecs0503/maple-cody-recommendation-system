from src.AvatarServer.AvatarProcessor.avatar_processor import AvatarProcessor
from src.AvatarServer.AvatarProcessor.packed_character_info import PackedCharacterInfo
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

    async def get_avatar_image(self, avatar: Avatar, ActionQuery: Optional[str] = None):
        return None


@pytest.fixture
def caller_for_test() -> CallerForTest:
    return CallerForTest()


@pytest.fixture
def avatar_processor_for_test(config_for_test: Config, caller_for_test: CallerForTest) -> AvatarProcessor:
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

    """
        TODO, FIXME: user 3에 대해 아래 정답으로도 pass 되어야 함
        아직 복호화 로직을 몰라서 추후 처리 예정
        packed_info.json:
        "hair_mix_color": -1 -> 6,
        "hair_mix_ratio": -1 -> 50
        avatar_info.json:
        "hair": "30005" -> "30005+6*50"
    """
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


def test_get_avatar():
    cwd = os.path.dirname(__file__)
    json_path = os.path.join(cwd, 'testdata', 'packed_info.json')

    with open(json_path, 'r') as file:
        data: dict = json.load(file)

    result_json_path = os.path.join(cwd, 'testdata', 'avatar_info.json')

    with open(result_json_path, 'r') as file:
        expected_data: dict = json.load(file)

    for user_name, user_data in data.items():
        input_data = PackedCharacterInfo()
        for k, v in user_data.items():
            if k == "str":
                continue
            setattr(input_data, k, v)
        avatar = input_data.get_avatar()
        for k, v in expected_data[user_name].items():
            assert getattr(avatar, k) == v


@pytest.mark.asyncio
def test_process_image():
    # TODO: implement
    pass
