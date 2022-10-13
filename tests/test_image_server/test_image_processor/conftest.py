import json
import logging
from typing import Optional

import pytest
from src.ImageServer.util.item_manager import ItemManager
from src.ImageServer.Avatar.avatar import Avatar
from src.ImageServer.ImageProcessor.WCR_caller import WCRCaller
import aiohttp
from src.ImageServer.ImageProcessor.image_processor import ImageProcessor
from src.ImageServer.server.config import Config
from PIL import Image
import os


class CallerForTest:
    """
    이 Caller은 어떤 것을 해야하냐면
    get_image 함수를 모킹
    아이템 코드들에 대해 사전에 준비된 이미지를 반환하면 됨
    없으면 exception

    아래 아이템에 대한 이미지들이 test_data에 저장되어 있어야 함
      - 용용 아이스 머리띠
      - 딸기 생크림
      - 투명 안경
      - 투명 귀고리
      - 어둠의 흉터
      - 프레피 멜빵
      - 투명 블레이드
      - 투명 장갑
      - 핑크 젤리백
      - 지나간 어둠
      - 믹스 토벤 머리 검은색 84 주황색 16
      - 믹스 도전적인 얼굴 파란색 50 에메랄드 50
      - 홍조 꽃잎 피부

    저 데이터는 인구가 줄 예정
    """

    def __init__(self):
        base_uri = os.path.dirname(__file__)
        item1_path = os.path.join(base_uri, "test_data", "item", "item1.png")
        self.image_1 = Image.open(item1_path)

    async def get_image(self, avatar: Avatar, ActionQuery: Optional[str] = None):
        URL = "https://localhost:7209/{item}/?code={code}&bs=True"
        params = avatar.to_param()
        if ActionQuery is not None:
            URL += "&actionName="
            URL += ActionQuery
        for idx in range(len(params)):
            if int(params[idx][1]) > 0:
                code_params = params[idx]
        # 무기 처리 코드 추가
        async with aiohttp.ClientSession() as session:
            async with session.get(URL.format(item=code_params[0], code=code_params[1]), ssl=False) as resp:
                if resp.status == 200:
                    return await resp.text()


@pytest.fixture
def caller_for_test():
    return CallerForTest()


@pytest.fixture
def test_image_processor(config_for_test: Config, caller_for_test: CallerForTest):
    # mocking된 Caller를 인자로 갖는 ImageProcessor을 반환
    # caller_for_test=caller_for_test()
    logger = logging.getLogger(__name__)
    base_uri = os.path.dirname(__file__)
    raw_json_path = os.path.join(base_uri, "base_wz_code.json")
    data_json_path = os.path.join(base_uri, "valid_wz_code.json")

    item_manager = ItemManager()

    res = ImageProcessor(
        logger=logger,
        config=config_for_test,
        item_manager=item_manager,
    )

    res.caller = caller_for_test
    res.item_manager.caller = caller_for_test

    if os.path.isfile(data_json_path):
        with open(data_json_path, "r", encoding="UTF-8") as file:
            data = json.load(file)
            item_manager.read(data)
    elif os.path.isfile(raw_json_path):
        with open(raw_json_path, "r", encoding="UTF-8") as file:
            data = json.load(file)
            item_manager.read_raw(data)

    return res


class ImageProcessorForTest:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
    ):
        self.logger = logger
        self.caller = WCRCaller(
            logger=self.logger,
            wcr_server_host=config.wcr_server_host,
            wcr_server_protocol=config.wcr_server_protocol,
            wcr_server_port=config.wcr_server_port,
            retry_num=config.wcr_caller_retry_num,
            timeout=config.wcr_caller_timeout,
            backoff=config.wcr_caller_backoff,
        )

    async def infer(self, image: Image) -> Avatar:
        result = Avatar("1", "1", "1", "1")
        return result


@pytest.fixture
def image_processor(config_for_test: Config):
    logger = logging.getLogger(__name__)
    result = ImageProcessorForTest(
        logger=logger,
        config=config_for_test,
    )
    return result
