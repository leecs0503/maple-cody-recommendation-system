import asyncio
import logging
import random
import json
import os
from heapq import heappush, heappop
from ..util import item_manager
from ..util.item_manager import ItemManager
from ..server.config import Config
from ..Avatar.avatar import Avatar
from .WCR_caller import WCRCaller
from PIL import Image
from typing import List, Tuple
import base64
import io
import multiprocessing


PIXEL = Tuple[int, int, int, int]


def is_pixel_eq(
    a: PIXEL,
    b: PIXEL,
):
    return abs(a[0] - b[0]) < 8 and \
           abs(a[1] - b[1]) < 8 and \
           abs(a[2] - b[2]) < 8 and \
           abs(a[3] - b[3]) < 8


def _get_pixel_list(
    pixel_data: List[PIXEL],
    height: int,
    width: int,
):
    item_coord = [(idx % height, idx // height, pixel) for idx, pixel in enumerate(pixel_data) if pixel[3] != 0]
    num_item_pixel = len(item_coord)

    # PIXEL 크기 1인 이미지는 is_contained 로직으로 판단하기 어렵기 때문에,
    # 1 pixel인 경우도 빈 리스트를 반환.
    if num_item_pixel <= 1:
        return []

    assert num_item_pixel > 0
    return item_coord


def _get_ratio(
    pivot_row: int,
    pivot_col: int,
    avatar_pixel_data: List[PIXEL],
    avatar_height: int,
    avatar_width: int,
    xy_list: List[Tuple[int, int, PIXEL]],
):
    correct_count = 0
    for dx, dy, item_pixel in xy_list:
        x = pivot_row + dx
        y = pivot_col + dy
        if x >= avatar_height or y >= avatar_width:
            continue
        avatar_pixel = avatar_pixel_data[y * avatar_height + x]
        if is_pixel_eq(avatar_pixel, item_pixel):
            correct_count += 1

    ratio = correct_count / len(xy_list)
    return ratio


def is_contain_by_list(
    avatar_pixel_list: List[PIXEL],
    avatar_size: Tuple[int, int],
    item_pixel_list: List[PIXEL],
    item_size: Tuple[int, int],
) -> Tuple[int, int, int]:
    SAMPLE_SIZE = 10
    VALIDATE_SAMPLE_NUM = 3
    [avatar_height, avatar_width] = avatar_size
    [item_height, item_width] = item_size

    all_item_pixel_xy_list = _get_pixel_list(item_pixel_list, item_height, item_width)

    if len(all_item_pixel_xy_list) == 0:
        return (0, 0, 0)

    sample_idx = random.sample(range(len(all_item_pixel_xy_list)), min(SAMPLE_SIZE, len(all_item_pixel_xy_list)))
    sample_item_pixel_xy_list = [all_item_pixel_xy_list[i] for i in sorted(sample_idx)]

    data = []
    for pivot_col in range(avatar_width):
        for pivot_row in range(avatar_height):
            ratio = _get_ratio(
                pivot_row=pivot_row,
                pivot_col=pivot_col,
                avatar_pixel_data=avatar_pixel_list,
                avatar_height=avatar_height,
                avatar_width=avatar_width,
                xy_list=sample_item_pixel_xy_list,
            )
            heappush(data, (ratio, pivot_row, pivot_col))
            if len(data) > VALIDATE_SAMPLE_NUM:
                heappop(data)

    result = (0, 0, 0)
    for ratio, pivot_row, pivot_col in data:
        correct_ratio = _get_ratio(
            pivot_row=pivot_row,
            pivot_col=pivot_col,
            avatar_pixel_data=avatar_pixel_list,
            avatar_height=avatar_height,
            avatar_width=avatar_width,
            xy_list=all_item_pixel_xy_list,
        )
        result = max(result, (correct_ratio, pivot_row, pivot_col))
    return result


def is_contain(
    avatar_image: Image.Image,
    item_image: Image.Image,
) -> Tuple[int, int, int]:
    if avatar_image is None or item_image is None:
        return (0, 0, 0)

    avatar_pixel_list = list(avatar_image.getdata())
    item_pixel_list = list(item_image.getdata())

    return is_contain_by_list(
        avatar_pixel_list=avatar_pixel_list,
        avatar_size=avatar_image.size,
        item_pixel_list=item_pixel_list,
        item_size=item_image.size,
    )


def _is_contain(
    avatar_image: Image.Image,
    item_image: Image.Image,
    code: str,
) -> Tuple[Tuple[int, int, int], str]:
    return is_contain(avatar_image, item_image), code


class ImageProcessor:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
    ):
        self.logger = logger
        self.base_wz_code_path = config.base_wz_code_path
        self.caller = WCRCaller(
            logger=self.logger,
            wcr_server_host=config.wcr_server_host,
            wcr_server_protocol=config.wcr_server_protocol,
            wcr_server_port=config.wcr_server_port,
            retry_num=config.wcr_caller_retry_num,
            timeout=config.wcr_caller_timeout,
            backoff=config.wcr_caller_backoff,
        )
        self.item_code_list = []
        self.item_manager = ItemManager(
            caller=self.caller
        )
        self.pool = multiprocessing.Pool(10)
        loop = asyncio.get_event_loop()
        base_wz = loop.run_until_complete(
            self._load_base_wz()
        )
        self.item_manager.read_raw(base_wz)
        loop.run_until_complete(
            self.item_manager.validate()
        )
        print(self.item_manager.data)

    async def _load_base_wz(self) -> dict:
        if self.base_wz_code_path:
            if os.path.isfile(self.base_wz_code_path):
                base_wz_code_path = self.base_wz_code_path
                with open(base_wz_code_path) as f:
                    base_wz = json.load(f)
                    return base_wz

        base_wz = await self.caller.get_base_wz()

        if self.base_wz_code_path:
            with open(self.base_wz_code_path, "w") as f:
                json.dump(base_wz, f, ensure_ascii=False, indent="\t")
        return base_wz

    def _visualize_correct(self, base_image: Image.Image, test_image: Image.Image):
        base_uri = os.path.dirname(__file__)

        acc, px, py = is_contain(base_image, test_image)
        test_format = base_image.copy()
        (h, w) = test_image.size
        pixels = test_format.load()
        for x in range(h):
            for y in range(w):
                ax, ay = (px + x, py + y)
                pa = base_image.getpixel((ax, ay))
                ta = test_image.getpixel((x, y))
                if not is_pixel_eq(pa, ta):
                    pixels[ax, ay] = (100, 100, 100, pixels[ax, ay][3])

        visualize_path = os.path.join(base_uri, "correct_visualize", "visualize.png")

        test_format.save(visualize_path)
        return acc

    async def image_of(self, avatar: Avatar):
        # FIXME: naming: _of suffix는 side effect가 없어야 함
        wcr_response = await self.caller.get_image(avatar=avatar)
        if wcr_response is None:
            return None

        image_data = base64.b64decode(wcr_response)
        item_image = Image.open(io.BytesIO(image_data))
        return item_image

    async def infer_sub(self, image: Image.Image, avatar: Avatar, code: str) -> Tuple[Tuple[int, int, int], str]:
        item_image = await self.image_of(avatar=avatar)
        if item_image is None:
            return ((0, 0, 0), "0")
        acc = is_contain(avatar_image=image, item_image=item_image), code
        return acc

    def max_acc_code(self, acc_list: List[Tuple[Tuple[int, int, int], str]]) -> Tuple[int, int]:
        max_acc = 0
        max_idx_acc = "0"
        for acc in acc_list:
            if acc[0][0] >= max_acc:
                max_acc = acc[0][0]
                max_idx_acc = acc[1]
        return max_acc, max_idx_acc

    async def save_all_image(self):
        # FIXME: refactoring
        BK_SIZE = 20
        for item_num in range(item_manager.NUM_ITEM):
            item_list = self.item_manager.get_item_list(idx=item_num)
            for idx in range(0, len(item_list), BK_SIZE):
                coroutines = []
                for code in item_list[idx:idx + BK_SIZE]:
                    avatar = Avatar()
                    avatar.add_parts(item_num, code)
                    coroutines.append(self.image_of(avatar))
                wcr_images = await asyncio.gather(*coroutines)
                for v, wcr_image in enumerate(wcr_images):
                    os.makedirs(os.path.join('.', '.data', f'parts{item_num}'), exist_ok=True)
                    if wcr_image:
                        wcr_image.save(os.path.join('.', '.data', f'parts{item_num}', f'item{idx+v}.png'))

    def process_wcr_images(
        self,
        image: Image.Image,
        wcr_images: List[Image.Image],
        item_list: List[str],
    ) -> Tuple[Tuple[int, int, int], str]:
        query = [
            (
                image,
                wcr_image,
                item_code
            )
            for wcr_image, item_code in zip(wcr_images, item_list)
        ]
        result = self.pool.starmap(_is_contain, query)
        return result

    async def infer(self, image: Image.Image) -> Avatar:
        # FIXME: 현재 autoscale metric에 부적합한 구조 수정 필요
        avatar = Avatar()
        result_part = []
        for item_num in range(item_manager.NUM_ITEM):
            acc_list: Tuple[Tuple[int, int, int], str] = []
            item_list = self.item_manager.get_item_list(idx=item_num)
            BK_SIZE = 20
            for idx in range(0, len(item_list), BK_SIZE):
                coroutines = [
                    self.image_of(Avatar.single_item_avatar_of(item_num, code))
                    for code in item_list[idx:idx + BK_SIZE]
                ]
                wcr_images = await asyncio.gather(*coroutines)

                result = self.process_wcr_images(
                    image=image,
                    wcr_images=wcr_images,
                    item_list=item_list[idx:idx + BK_SIZE]
                )
                acc_list += result
            _, max_acc_idx = self.max_acc_code(acc_list)
            result_part.append(max_acc_idx)
        for idx, max_acc_idx in enumerate(result_part):
            avatar.add_parts(idx, max_acc_idx)
        return avatar
