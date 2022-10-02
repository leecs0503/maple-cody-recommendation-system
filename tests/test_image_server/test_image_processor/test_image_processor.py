import os

import pytest
from PIL import Image
from src.ImageServer.Avatar.avatar import Avatar

from src.ImageServer.ImageProcessor.image_processor import ImageProcessor


# WCR Server을 mocking새ㅓ
@pytest.mark.asyncio
async def test_is_contain(test_image_processor: ImageProcessor):
    # image 1 로드
    # image 2 로드
    # 아이템 1~7 이미지 로드
    base_uri = os.path.dirname(__file__)
    data1_path = os.path.join(base_uri, 'test_data', 'data1.png')
    data2_path = os.path.join(base_uri, 'test_data', 'data2.png')
    item1_path = os.path.join(base_uri, 'test_data', 'item1.png')
    item2_path = os.path.join(base_uri, 'test_data', 'item2.png')
    item3_path = os.path.join(base_uri, 'test_data', 'item3.png')
    item4_path = os.path.join(base_uri, 'test_data', 'item4.png')

    image_1 = Image.open(data1_path)
    image_2 = Image.open(data2_path)
    item_1 = Image.open(item1_path)
    item_2 = Image.open(item2_path)
    item_3 = Image.open(item3_path)
    item_4 = Image.open(item4_path)
#    item_5 = Image.open('./test_data/item5.png')
#    item_6 = Image.open('./test_data/item6.png')
#    item_7 = Image.open('./test_data/item7.png')
#    item_8 = Image.open('./test_data/item8.png')

    avatar_list = [
        image_1, image_2
    ]
    item_list = [
        item_1 , item_2 , item_3 , item_4
    ]
    for idx, avatar in enumerate(avatar_list):
        for item in item_list:
            assert await test_image_processor.is_contain(avatar, item) == True
#            assert await test_image_processor.is_contain(avatar, item) == (True if idx == 0 else False)


@pytest.mark.asyncio
async def test_infer(test_image_processor: ImageProcessor):
    base_uri = os.path.dirname(__file__)
    data1_path = os.path.join(base_uri, 'test_data', 'data1.png')

    image_1 = Image.open(data1_path)

    result = await test_image_processor.infer(image_1)

    assert result == Avatar("1" , "0" , "0" , "0")


@pytest.mark.asyncio
async def test_image_processor(image_processor: ImageProcessor):
    base_uri = os.path.dirname(__file__)
    data1_path = os.path.join(base_uri, 'test_data', 'data1.png')

#    now_path = os.path.join(os.getcwd(), "tests", "test_image_server", "test_image_processor")
#    data_path = os.path.join(now_path, "test_data", "data1.png")
    image = Image.open(data1_path)

    result = await image_processor.infer(image)
    assert result.to_array() == ["1", "1", "1", "1"]
