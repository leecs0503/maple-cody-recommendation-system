import os
import pytest
from PIL import Image

from src.ImageServer.ImageProcessor.image_processor import ImageProcessor


@pytest.mark.asyncio
async def test_is_contain(test_image_processor: ImageProcessor):
    # image 1 로드
    # image 2 로드
    # 아이템 1~7 이미지 로드
    NUM_USER = 30
    NUM_HIGH = 5
    base_uri = os.path.dirname(__file__)

    for idx in range(1, NUM_USER + 1):
        globals()[f"data{idx}_path"] = os.path.join(base_uri, "test_data", f"data{idx}.png")

    item1_path = os.path.join(base_uri, "test_data", "item1.png")
    item2_path = os.path.join(base_uri, "test_data", "item2.png")
    item3_path = os.path.join(base_uri, "test_data", "item3.png")
    item4_path = os.path.join(base_uri, "test_data", "item4.png")
    item5_path = os.path.join(base_uri, "test_data", "item5.png")
    item6_path = os.path.join(base_uri, "test_data", "item6.png")
    item7_path = os.path.join(base_uri, "test_data", "item7.png")
    item8_path = os.path.join(base_uri, "test_data", "item8.png")

    test_item4_path = os.path.join(base_uri, "test_data", "test_item4.png")

    for idx in range(1, NUM_USER + 1):
        globals()[f"image_{idx}"] = Image.open(globals()[f"data{idx}_path"])

    item_1 = Image.open(item1_path)
    item_2 = Image.open(item2_path)
    item_3 = Image.open(item3_path)
    item_4 = Image.open(item4_path)
    item_5 = Image.open(item5_path)
    item_6 = Image.open(item6_path)
    item_7 = Image.open(item7_path)
    item_8 = Image.open(item8_path)

    # fmt: off
    avatar_list = [image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9, image_10, image_11, image_12, image_13, image_14, image_15, image_16, image_17, image_18, image_19, image_20, image_21, image_22, image_23, image_24, image_25, image_26, image_27, image_28, image_29, image_30]
    # fmt: on
    item_list = [
        item_1,
        item_2,
        item_3,
        item_4,
        item_5,
        item_6,
        item_7,
        item_8,
    ]

    for item_idx, item in enumerate(item_list):
        accuracy = []
        for idx, avatar in enumerate(avatar_list):
            item_accuracy = await test_image_processor.is_contain(avatar, item, "sample")
            print("avatar_idx : ", idx + 1)
            print("item_idx : ", item_idx + 1)
            print("method : sample")
            accuracy.append(item_accuracy)
        else:
            high_accuracies = sorted(range(len(accuracy)), key=lambda i: accuracy[i], reverse=True)[: NUM_HIGH - 1]

            high_accuracy = []
            for high_idx in high_accuracies:
                high_avatar = avatar_list[high_idx]
                high_item_accuracy = await test_image_processor.is_contain(high_avatar, item, "naive")
                print("high_avatar_idx : ", high_idx + 1)
                print("item_idx : ", item_idx + 1)
                print("method : highest_naive")
                high_accuracy.append(high_item_accuracy)
                if high_idx == 0:
                    base_accuracy = high_item_accuracy
            else:
                # base_accuracy = await test_image_processor.is_contain(avatar_list[0], item, 'naive')

                largest_accuracy = max(high_accuracy)
                print("!!!!!!!!!!!")
                print("largest_accuracy : ", largest_accuracy)
                print("!!!!!!!!!!!")
                assert largest_accuracy == base_accuracy


@pytest.mark.asyncio
async def test_image_processor(image_processor: ImageProcessor):
    base_uri = os.path.dirname(__file__)
    data1_path = os.path.join(base_uri, "test_data", "data1.png")

    #    now_path = os.path.join(os.getcwd(), "tests", "test_image_server", "test_image_processor")
    #    data_path = os.path.join(now_path, "test_data", "data1.png")
    image = Image.open(data1_path)

    result = await image_processor.infer(image)
    assert result.to_array() == ["1", "1", "1", "1"]
