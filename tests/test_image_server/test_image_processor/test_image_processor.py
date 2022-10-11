import os
import pytest
import time
import numpy as np
from PIL import Image

from src.ImageServer.Avatar.avatar import Avatar
from src.ImageServer.ImageProcessor.image_processor import ImageProcessor, is_pixel_eq
from pathlib import Path


@pytest.mark.asyncio
async def test_visualize(test_image_processor: ImageProcessor):

    base_uri = os.path.dirname(__file__)

    base_image_path = os.path.join(base_uri, "test_data", "avatar", "data1.png")
    base_image = Image.open(base_image_path)
    visual_test1_path = os.path.join(base_uri, "test_data", "visual_test1.png")
    visual_test2_path = os.path.join(base_uri, "test_data", "visual_test2.png")

    visual_test1_image = Image.open(visual_test1_path)
    visual_test2_image = Image.open(visual_test2_path)

    parent_uri = Path(base_uri).parent.parent.parent
    visualize_parent = parent_uri.joinpath("src", "ImageServer", "ImageProcessor", "correct_visualize", "visualize.png")

    test1_acc = test_image_processor._correct_visualize(base_image, visual_test1_image)
    visualize_image = Image.open(visualize_parent)
    correct_visual1_acc = test_image_processor.is_contain(visualize_image, visual_test1_image)

    test2_acc = test_image_processor._correct_visualize(base_image, visual_test2_image)
    visualize_image = Image.open(visualize_parent)
    correct_visual2_acc = test_image_processor.is_contain(visualize_image, visual_test2_image)

    assert (test1_acc == correct_visual1_acc[0]) and (test2_acc == correct_visual2_acc[0])


@pytest.mark.asyncio
async def test_is_contain(test_image_processor: ImageProcessor):
    NUM_USER = 10
    NUM_ITEM = 8
    NUM_SKIN = 20
    base_uri = os.path.dirname(__file__)

    item_path = [os.path.join(base_uri, "test_data", "item", f"item{idx + 1}.png") for idx in range(NUM_ITEM)]
    user_path = [os.path.join(base_uri, "test_data", "avatar", f"data{idx + 1}.png") for idx in range(NUM_USER)]
    skin_path = [os.path.join(base_uri, "test_data", "skin", f"피부{idx + 1}.png") for idx in range(NUM_SKIN)]
    test_path = os.path.join(base_uri, "test_data", "test.png")

    item_list = [Image.open(path) for path in item_path]
    skin_list = [Image.open(path) for path in skin_path]
    avatar_list = [Image.open(path) for path in user_path]
    test_image = Image.open(test_path)
    item_name = [
        "모자",
        "무기",
        "몸통",
        "가방",
        "신발",
        "머리",
        "눈",
        "피부",
    ]
    print("")

    for avatar in avatar_list:
        img = np.array(avatar)
        idx = np.where(img[:, :, 3] > 0)
        x0, y0, x1, y1 = idx[1].min(), idx[0].min(), idx[1].max(), idx[0].max()
        avatar = Image.fromarray(img[y0:y1+1, x0:x1+1, :])

    avatar_pixel_list = [(list(avatar.getdata()), avatar.size[0], avatar.size[1]) for avatar in avatar_list]
    skin_pixel_list = [(list(skin.getdata()), skin.size[0], skin.size[1]) for skin in skin_list]

    ct = time.time()

    for idx, (avatar, avatar_height, avatar_width) in enumerate(avatar_pixel_list):
        for skin_idx, (skin, skin_height, skin_width) in enumerate(skin_pixel_list):
            skin_accuracy, _, _ = test_image_processor.is_contain(avatar, avatar_height, avatar_width, skin, skin_height, skin_width)
        #     print(f"idx: {idx + 1}, item: {skin_idx + 1} acc: {skin_accuracy: .3f}")
        # print("-" * 30)
    # assert test_image_processor.is_contain(avatar_list[0], avatar_list[0]) == 1
    print(time.time() - ct)
    return
    for item_idx, item in enumerate(item_list):
        for idx, avatar in enumerate(avatar_list):
            item_accuracy, _, _ = test_image_processor.is_contain(avatar, item)
            print(f"idx: {idx + 1}, item: {item_name[item_idx]} acc: {item_accuracy: .3f}")
        print("-" * 30)


@pytest.mark.asyncio
async def test_infer(test_image_processor: ImageProcessor):
    NUM_FACE = 20000
    NUM_CAP = 1004999
    NUM_LONGCOAT = 1052975
    NUM_WEAPON = 1703238
    NUM_COMPARE = 50

    num_items = (NUM_FACE, NUM_CAP, NUM_LONGCOAT, NUM_WEAPON)

    base_uri = os.path.dirname(__file__)

    user_path = os.path.join(base_uri, "test_data", "avatar", "data1.png")
    avatar_image = Image.open(user_path)

    item_list = []
    for idx, num_item in enumerate(num_items):
        for code_idx in range(num_item - NUM_COMPARE, num_item + NUM_COMPARE):
            item_list.append((idx, f"{code_idx}"))

    result = test_image_processor.infer(avatar_image, item_list)
    assert await result == Avatar(f"{NUM_FACE}", f"{NUM_CAP}", f"{NUM_LONGCOAT}", f"{NUM_WEAPON}")
