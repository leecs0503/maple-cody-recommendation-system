import os
import pytest
from PIL import Image

from src.ImageServer.ImageProcessor.image_processor import ImageProcessor, is_pixel_eq


@pytest.mark.asyncio
async def test_is_contain(test_image_processor: ImageProcessor):
    NUM_USER = 10
    NUM_ITEM = 8
    NUM_SKIN = 20
    base_uri = os.path.dirname(__file__)

    item_path = [
        os.path.join(base_uri, "test_data", "item", f"item{idx + 1}.png")
        for idx in range(NUM_ITEM)
    ]
    user_path = [
        os.path.join(base_uri, "test_data", "avatar", f"data{idx + 1}.png")
        for idx in range(NUM_USER)
    ]
    skin_path = [
        os.path.join(base_uri, "test_data", "skin", f"피부{idx + 1}.png")
        for idx in range(NUM_SKIN)
    ]
    test_path = os.path.join(base_uri, "test_data", f"test.png")

    item_list = [
        Image.open(path)
        for path in item_path
    ]
    skin_list = [
        Image.open(path)
        for path in skin_path
    ]
    avatar_list = [
        Image.open(path)
        for path in user_path
    ]
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
    
    acc, px, py = test_image_processor.is_contain(avatar_list[0], test_image)
    test_format = avatar_list[0].copy()
    (h, w) = test_image.size
    
    pixels = test_format.load()
    for x in range(h):
        for y in range(w):
            ax, ay = (px + x, py + y)
            pa = avatar_list[0].getpixel((ax, ay))
            ta = test_image.getpixel((x, y))
            if not is_pixel_eq(pa, ta):
              pixels[ax, ay] = (255 - pixels[ax, ay][0] , 255 - pixels[ax, ay][1], 255 - pixels[ax, ay][2], pixels[ax, ay][3])
    test_format.save('./visualize.png')
    print(f"original - made acc: {acc}")
    for idx, avatar in enumerate(avatar_list):
        for skin_idx, skin in enumerate(skin_list):
            skin_accuracy, _, _ = test_image_processor.is_contain(avatar, skin)
            print(f"idx: {idx + 1}, item: {skin_idx + 1} acc: {skin_accuracy: .3f}")
        print("-"*30)
    # assert test_image_processor.is_contain(avatar_list[0], avatar_list[0]) == 1
    return
    for item_idx, item in enumerate(item_list):
        for idx, avatar in enumerate(avatar_list):
            item_accuracy, _, _ = test_image_processor.is_contain(avatar, item)
            print(f"idx: {idx + 1}, item: {item_name[item_idx]} acc: {item_accuracy: .3f}")
        print("-"*30)